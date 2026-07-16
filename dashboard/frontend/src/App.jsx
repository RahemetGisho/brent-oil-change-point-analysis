import { useState, useMemo } from "react";
import Header from "./components/Header";
import KpiCards from "./components/KpiCards";
import FilterBar from "./components/FilterBar";
import PriceChart from "./components/PriceChart";
import EventList from "./components/EventList";
import EventDetailDrawer from "./components/EventDetailDrawer";
import ChangePointSummary from "./components/ChangePointSummary";
import RegimePanel from "./components/RegimePanel";
import {
  usePrices,
  useEvents,
  useEventCategories,
  useChangePoints,
  useRegimes,
  useMetrics,
} from "./hooks";

const DEFAULT_RANGE = { start: "1987-05-20", end: "2022-11-14" };

export default function App() {
  const [dateRange, setDateRange] = useState(DEFAULT_RANGE);
  const [activeCategory, setActiveCategory] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const resample = useMemo(() => {
    const days =
      (new Date(dateRange.end).getTime() - new Date(dateRange.start).getTime()) / 86400000;
    if (days > 365 * 6) return "M";
    if (days > 365) return "W";
    return "D";
  }, [dateRange]);

  const { data: priceData, loading: pricesLoading, error: pricesError } = usePrices({
    ...dateRange,
    resample,
  });
  const { data: eventData, loading: eventsLoading } = useEvents({
    category: activeCategory,
    ...dateRange,
  });
  const { data: categoryData } = useEventCategories();
  const { data: changePoints, loading: cpLoading } = useChangePoints();
  const { data: regimes, loading: regimesLoading } = useRegimes();
  const { data: metrics, loading: metricsLoading } = useMetrics();

  const apiOk = !pricesError;

  function handleReset() {
    setDateRange(DEFAULT_RANGE);
    setActiveCategory(null);
    setSelectedEvent(null);
  }

  return (
    <div className="app-shell">
      <Header apiOk={apiOk} />
      <main className="app-main">
        <KpiCards metrics={metrics} loading={metricsLoading} />

        <div className="panel">
          <FilterBar
            dateRange={dateRange}
            onDateRangeChange={setDateRange}
            categories={categoryData?.categories || []}
            activeCategory={activeCategory}
            onCategoryChange={setActiveCategory}
            onReset={handleReset}
          />
        </div>

        <div className="content-grid">
          <div className="panel">
            <div className="panel__header">
              <div>
                <div className="panel__title">Historical Brent Price with Detected Change Points</div>
                <div className="panel__subtitle">
                  Click any event marker to highlight its window on the chart
                </div>
              </div>
            </div>
            {pricesError ? (
              <div className="state-message">
                Could not reach the API — is the Flask backend running on port 5001?
              </div>
            ) : (
              <PriceChart
                prices={priceData?.data}
                changePoints={changePoints}
                events={eventData?.data}
                selectedEvent={selectedEvent}
                onSelectEvent={setSelectedEvent}
              />
            )}
          </div>

          <div className="panel">
            <div className="panel__header">
              <div>
                <div className="panel__title">Event Calendar</div>
                <div className="panel__subtitle">{eventData?.count ?? "…"} events in range</div>
              </div>
            </div>
            <EventList
              events={eventData?.data}
              loading={eventsLoading}
              selectedEvent={selectedEvent}
              onSelectEvent={setSelectedEvent}
            />
          </div>
        </div>

        <div className="panel">
          <div className="panel__header">
            <div>
              <div className="panel__title">Bayesian Change Point Model Results</div>
              <div className="panel__subtitle">
                PyMC single change-point models (discrete-uniform prior over the switch date)
              </div>
            </div>
          </div>
          <ChangePointSummary changePoints={changePoints} loading={cpLoading} />
        </div>

        <div className="panel">
          <div className="panel__header">
            <div>
              <div className="panel__title">Markov-Switching Cross-Validation</div>
              <div className="panel__subtitle">
                Independently-detected turbulent regimes, matched to the nearest known event
              </div>
            </div>
          </div>
          <RegimePanel regimes={regimes} loading={regimesLoading} />
        </div>
      </main>

      {selectedEvent && (
        <EventDetailDrawer event={selectedEvent} onClose={() => setSelectedEvent(null)} />
      )}
    </div>
  );
}
