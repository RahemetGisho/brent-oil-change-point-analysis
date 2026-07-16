"""
app.api.events — the researched event calendar and its quantified impact.

Endpoints
---------
GET /api/v1/events
    Query params:
        category (optional) — filter by event category (e.g. "Conflict")
        start, end (YYYY-MM-DD, optional) — filter by event start_date range
    Returns the compiled event list, each merged with its empirical
    before/after price & volatility impact (event correlation data).

GET /api/v1/events/<id>
    Returns a single event with full detail + impact stats.

GET /api/v1/events/categories
    Returns the distinct list of event categories (for building a filter UI).
"""

from flask import Blueprint, jsonify, request
import pandas as pd

from app.data.loader import get_events, get_event_by_id, get_event_impact_by_id

bp = Blueprint("events", __name__, url_prefix="/api/v1/events")


def _merge_impact(event: dict) -> dict:
    impact = get_event_impact_by_id(event["id"]) or {}
    merged = dict(event)
    merged["impact"] = {
        "price_before": impact.get("price_before"),
        "price_after": impact.get("price_after"),
        "pct_change": impact.get("pct_change"),
        "volatility_before_pct": impact.get("volatility_before_pct"),
        "volatility_after_pct": impact.get("volatility_after_pct"),
        "direction_confirmed": impact.get("direction_confirmed"),
    }
    return merged


@bp.get("")
def list_events():
    category = request.args.get("category")
    start = request.args.get("start")
    end = request.args.get("end")

    events = get_events()

    if category:
        events = [e for e in events if e["category"].lower() == category.lower()]
    if start:
        start_ts = pd.Timestamp(start)
        events = [e for e in events if pd.Timestamp(e["start_date"]) >= start_ts]
    if end:
        end_ts = pd.Timestamp(end)
        events = [e for e in events if pd.Timestamp(e["start_date"]) <= end_ts]

    merged = [_merge_impact(e) for e in events]
    merged.sort(key=lambda e: e["start_date"])
    return jsonify({"count": len(merged), "data": merged})


@bp.get("/categories")
def categories():
    events = get_events()
    cats = sorted({e["category"] for e in events})
    return jsonify({"categories": cats})


@bp.get("/<int:event_id>")
def get_event(event_id: int):
    event = get_event_by_id(event_id)
    if event is None:
        return jsonify({"error": f"event {event_id} not found"}), 404
    return jsonify(_merge_impact(event))
