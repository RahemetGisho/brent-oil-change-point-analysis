import { useMemo } from "react";
import {
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ReferenceArea,
  ReferenceDot,
  Brush,
  ResponsiveContainer,
} from "recharts";
import { formatUSD, formatDate, categoryColor } from "../utils/format";

function nearestPrice(prices, targetDate) {
  const target = new Date(targetDate).getTime();
  let best = null;
  let bestDiff = Infinity;
  for (const p of prices) {
    const diff = Math.abs(new Date(p.date).getTime() - target);
    if (diff < bestDiff) {
      bestDiff = diff;
      best = p;
    }
  }
  return best;
}

function CustomTooltip({ active, payload, label, eventsByDate }) {
  if (!active || !payload?.length) return null;
  const event = eventsByDate.get(label);
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip__date">{formatDate(label)}</div>
      <div className="chart-tooltip__row">
        <span>Price</span>
        <span>{formatUSD(payload[0].value)}</span>
      </div>
      {event && <div className="chart-tooltip__event">● {event.name}</div>}
    </div>
  );
}

export default function PriceChart({ prices, changePoints, events, selectedEvent, onSelectEvent }) {
  const eventsByDate = useMemo(() => {
    const map = new Map();
    for (const e of events || []) map.set(e.start_date, e);
    return map;
  }, [events]);

  const eventDots = useMemo(() => {
    if (!prices?.length || !events?.length) return [];
    return events
      .map((e) => {
        const match = nearestPrice(prices, e.start_date);
        return match ? { ...e, plotDate: match.date, plotPrice: match.price } : null;
      })
      .filter(Boolean);
  }, [prices, events]);

  if (!prices?.length) {
    return <div className="state-message">No price data for the selected range.</div>;
  }

  return (
    <div>
      <ResponsiveContainer width="100%" height={420}>
        <ComposedChart data={prices} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e7edf3" />
          <XAxis
            dataKey="date"
            tickFormatter={(d) => formatDate(d, { style: "short" })}
            minTickGap={40}
            tick={{ fontSize: 11, fill: "#64748b" }}
          />
          <YAxis
            tickFormatter={(v) => `$${v}`}
            width={54}
            tick={{ fontSize: 11, fill: "#64748b" }}
          />
          <Tooltip content={<CustomTooltip eventsByDate={eventsByDate} />} />

          {selectedEvent && (
            <ReferenceArea
              x1={selectedEvent.start_date}
              x2={selectedEvent.end_date || selectedEvent.start_date}
              fill={categoryColor(selectedEvent.category)}
              fillOpacity={0.15}
              stroke={categoryColor(selectedEvent.category)}
              strokeOpacity={0.4}
            />
          )}

          {changePoints?.mean_shift && (
            <ReferenceLine
              x={changePoints.mean_shift.tau_date}
              stroke="#1f4e79"
              strokeWidth={2}
              strokeDasharray="6 3"
              label={{ value: "Mean shift", position: "insideTopLeft", fontSize: 11, fill: "#1f4e79" }}
            />
          )}
          {changePoints?.variance_shift && (
            <ReferenceLine
              x={changePoints.variance_shift.tau_date}
              stroke="#c0392b"
              strokeWidth={2}
              strokeDasharray="6 3"
              label={{ value: "Volatility shift", position: "insideTopRight", fontSize: 11, fill: "#c0392b" }}
            />
          )}

          <Line
            type="monotone"
            dataKey="price"
            stroke="#1f4e79"
            strokeWidth={1.6}
            dot={false}
            isAnimationActive={false}
          />

          {eventDots.map((e) => (
            <ReferenceDot
              key={e.id}
              x={e.plotDate}
              y={e.plotPrice}
              r={selectedEvent?.id === e.id ? 7 : 4.5}
              fill={categoryColor(e.category)}
              stroke="#fff"
              strokeWidth={1.5}
              onClick={() => onSelectEvent(e)}
              style={{ cursor: "pointer" }}
            />
          ))}

          <Brush dataKey="date" height={26} stroke="#1f4e79" tickFormatter={(d) => formatDate(d, { style: "short" })} />
        </ComposedChart>
      </ResponsiveContainer>

      <div className="chart-legend">
        <span className="chart-legend__item">
          <span className="chart-legend__swatch" style={{ background: "#1f4e79" }} />
          Brent price
        </span>
        <span className="chart-legend__item">
          <span className="chart-legend__swatch" style={{ background: "#1f4e79", opacity: 0.6 }} />
          Mean-shift change point
        </span>
        <span className="chart-legend__item">
          <span className="chart-legend__swatch" style={{ background: "#c0392b", opacity: 0.6 }} />
          Volatility-shift change point
        </span>
        <span className="chart-legend__item">
          <span className="chart-legend__swatch" style={{ background: "#17A398", borderRadius: "50%", width: 8, height: 8 }} />
          Event marker (click to highlight)
        </span>
      </div>
    </div>
  );
}
