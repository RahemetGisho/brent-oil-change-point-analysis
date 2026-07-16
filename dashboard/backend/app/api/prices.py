"""
app.api.prices — historical Brent price data.

Endpoints
---------
GET /api/v1/prices
    Query params:
        start (YYYY-MM-DD, optional) — inclusive lower bound
        end   (YYYY-MM-DD, optional) — inclusive upper bound
        resample (D|W|M, optional, default D) — downsample frequency,
            useful for rendering long ranges without shipping 9,000+ points
    Returns: {"count": int, "resample": str, "data": [{"date": str, "price": float}, ...]}

GET /api/v1/prices/summary
    Returns summary statistics for the (optionally date-filtered) series:
    {"start_date", "end_date", "count", "min", "max", "mean", "latest"}
"""

from flask import Blueprint, jsonify, request
import pandas as pd

from app.data.loader import get_prices_df

bp = Blueprint("prices", __name__, url_prefix="/api/v1/prices")

_RESAMPLE_RULES = {"D": None, "W": "W", "M": "ME"}


def _filter_by_date(df: pd.DataFrame, start: str | None, end: str | None) -> pd.DataFrame:
    if start:
        df = df[df["Date"] >= pd.Timestamp(start)]
    if end:
        df = df[df["Date"] <= pd.Timestamp(end)]
    return df


@bp.get("")
def list_prices():
    start = request.args.get("start")
    end = request.args.get("end")
    resample = (request.args.get("resample") or "D").upper()

    if resample not in _RESAMPLE_RULES:
        return jsonify({"error": f"invalid resample '{resample}', expected one of D, W, M"}), 400

    df = get_prices_df()
    df = _filter_by_date(df, start, end)

    if df.empty:
        return jsonify({"count": 0, "resample": resample, "data": []})

    rule = _RESAMPLE_RULES[resample]
    if rule is not None:
        df = df.set_index("Date").resample(rule)["Price"].mean().dropna().reset_index()

    data = [
        {"date": d.strftime("%Y-%m-%d"), "price": round(float(p), 2)}
        for d, p in zip(df["Date"], df["Price"])
    ]
    return jsonify({"count": len(data), "resample": resample, "data": data})


@bp.get("/summary")
def prices_summary():
    start = request.args.get("start")
    end = request.args.get("end")

    df = get_prices_df()
    df = _filter_by_date(df, start, end)

    if df.empty:
        return jsonify({"error": "no data in the requested range"}), 404

    return jsonify({
        "start_date": df["Date"].min().strftime("%Y-%m-%d"),
        "end_date": df["Date"].max().strftime("%Y-%m-%d"),
        "count": int(len(df)),
        "min": round(float(df["Price"].min()), 2),
        "max": round(float(df["Price"].max()), 2),
        "mean": round(float(df["Price"].mean()), 2),
        "latest": round(float(df["Price"].iloc[-1]), 2),
    })
