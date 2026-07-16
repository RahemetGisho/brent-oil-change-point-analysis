const PRESETS = [
  { label: "All time", start: "1987-05-20", end: "2022-11-14" },
  { label: "2008 GFC", start: "2007-06-01", end: "2010-01-01" },
  { label: "2014–16 Collapse", start: "2014-01-01", end: "2016-12-31" },
  { label: "2020 COVID", start: "2019-10-01", end: "2020-12-31" },
  { label: "2022 Ukraine", start: "2021-09-01", end: "2022-11-14" },
];

export default function FilterBar({
  dateRange,
  onDateRangeChange,
  categories,
  activeCategory,
  onCategoryChange,
  onReset,
}) {
  const activePreset = PRESETS.find(
    (p) => p.start === dateRange.start && p.end === dateRange.end
  );

  return (
    <div className="filter-bar">
      <div className="filter-field">
        <label htmlFor="start-date">From</label>
        <input
          id="start-date"
          type="date"
          value={dateRange.start}
          min="1987-05-20"
          max={dateRange.end}
          onChange={(e) => onDateRangeChange({ ...dateRange, start: e.target.value })}
        />
      </div>
      <div className="filter-field">
        <label htmlFor="end-date">To</label>
        <input
          id="end-date"
          type="date"
          value={dateRange.end}
          min={dateRange.start}
          max="2022-11-14"
          onChange={(e) => onDateRangeChange({ ...dateRange, end: e.target.value })}
        />
      </div>

      <div className="range-presets">
        {PRESETS.map((p) => (
          <button
            key={p.label}
            className={`range-preset-btn ${activePreset?.label === p.label ? "range-preset-btn--active" : ""}`}
            onClick={() => onDateRangeChange({ start: p.start, end: p.end })}
          >
            {p.label}
          </button>
        ))}
      </div>

      <div className="filter-field" style={{ marginLeft: "auto" }}>
        <label htmlFor="category-select">Event category</label>
        <select
          id="category-select"
          value={activeCategory || ""}
          onChange={(e) => onCategoryChange(e.target.value || null)}
        >
          <option value="">All categories</option>
          {categories.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
      </div>

      <button className="btn-reset" onClick={onReset}>
        Reset filters
      </button>
    </div>
  );
}
