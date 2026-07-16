export default function Header({ apiOk }) {
  return (
    <header className="app-header">
      <div className="app-header__brand">
        <div className="app-header__logo">BE</div>
        <div>
          <div className="app-header__title">Brent Oil Intelligence</div>
          <div className="app-header__subtitle">Birhan Energies · Change Point Dashboard</div>
        </div>
      </div>
      <div className="app-header__status">
        <span className={`status-dot ${apiOk === false ? "status-dot--error" : ""}`} />
        {apiOk === false ? "API unreachable" : "Live data"}
      </div>
    </header>
  );
}
