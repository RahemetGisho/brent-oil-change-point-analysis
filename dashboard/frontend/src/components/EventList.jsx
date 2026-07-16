import { formatDate, formatPct, categoryColor } from "../utils/format";

export default function EventList({ events, loading, selectedEvent, onSelectEvent }) {
  if (loading) {
    return (
      <div className="event-list">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="skeleton" style={{ height: 46 }} />
        ))}
      </div>
    );
  }

  if (!events?.length) {
    return <div className="state-message">No events match the current filters.</div>;
  }

  return (
    <div className="event-list">
      {events.map((event) => {
        const pctChange = event.impact?.pct_change;
        const isSelected = selectedEvent?.id === event.id;
        return (
          <div
            key={event.id}
            className={`event-row ${isSelected ? "event-row--selected" : ""}`}
            onClick={() => onSelectEvent(isSelected ? null : event)}
          >
            <span
              className="event-row__category-dot"
              style={{ background: categoryColor(event.category) }}
            />
            <div className="event-row__body">
              <div className="event-row__name">{event.name}</div>
              <div className="event-row__date">
                {formatDate(event.start_date, { style: "short" })} · {event.category}
              </div>
            </div>
            {pctChange !== null && pctChange !== undefined && (
              <div
                className={`event-row__change ${
                  pctChange >= 0 ? "event-row__change--positive" : "event-row__change--negative"
                }`}
              >
                {formatPct(pctChange)}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
