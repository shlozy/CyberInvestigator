
import { useEffect, useState } from "react";

import {
  Shield,
  LayoutDashboard,
  Activity,
  AlertTriangle,
  Network,
  FileSearch,
  Settings,
  Search,
  Bell,
  ChevronDown,
  Clock,
  CircleDot,
  Monitor,
  Globe,
  ShieldCheck,
} from "lucide-react";

import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";
const ALERTS_URL = `${API_BASE_URL}/alerts`;
const NETWORK_EVENTS_URL = `${API_BASE_URL}/network-events`;

function App() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [eventsTotal, setEventsTotal] = useState(0);
  const [eventsLoading, setEventsLoading] = useState(true);
  const [eventsError, setEventsError] = useState("");

  useEffect(() => {
    async function fetchAlerts() {
      try {
        const response = await fetch(ALERTS_URL);

        if (!response.ok) {
          throw new Error("Failed to fetch alerts");
        }

        const data = await response.json();
        setAlerts(data.alerts || []);
        setError("");
      } catch (err) {
        console.error("API connection error:", err);
        setError("Unable to connect to the Cyber Investigator API.");
      } finally {
        setLoading(false);
      }
    }

    async function fetchNetworkEvents() {
      try {
        const response = await fetch(NETWORK_EVENTS_URL);

        if (!response.ok) {
          throw new Error("Failed to fetch network events");
        }

        const data = await response.json();
        const events = Array.isArray(data.events) ? data.events : [];

        // Prefer the backend's count; fall back to the returned records.
        setEventsTotal(
          typeof data.total === "number" ? data.total : events.length
        );
        setEventsError("");
      } catch (err) {
        console.error("Network events API error:", err);
        setEventsError("Unable to load network events.");
      } finally {
        setEventsLoading(false);
      }
    }

    // Both requests start immediately and finish independently.
    fetchAlerts();
    fetchNetworkEvents();
  }, []);

  const apiLoading = loading || eventsLoading;
  const failedRequests = [error, eventsError].filter(Boolean).length;

  let apiStatus = "connected";

  if (apiLoading) {
    apiStatus = "connecting";
  } else if (failedRequests === 2) {
    apiStatus = "offline";
  } else if (failedRequests === 1) {
    apiStatus = "partial";
  }

  const statusBanner = {
    connecting: {
      title: "Connecting to investigation backend...",
      message: "Retrieving saved alerts and network events.",
      label: "CONNECTING",
      card: "...",
    },
    connected: {
      title: "Investigation workspace connected",
      message:
        "Your dashboard is receiving saved alerts and network events from the backend.",
      label: "LIVE API",
      card: "Connected",
    },
    partial: {
      title: "Backend partially available",
      message: `${error ? "Saved alerts" : "Network events"} could not be loaded. Check the FastAPI server output.`,
      label: "PARTIAL",
      card: "Partial",
    },
    offline: {
      title: "Backend connection unavailable",
      message: "Check that the FastAPI server is running.",
      label: "OFFLINE",
      card: "Offline",
    },
  }[apiStatus];

  const openAlerts = alerts.filter(
    (alert) => alert.status === "OPEN"
  ).length;

  const reviewedAlerts = alerts.filter(
    (alert) => alert.status === "REVIEWED"
  ).length;

  const closedAlerts = alerts.filter(
    (alert) => alert.status === "CLOSED"
  ).length;

  const stats = [
    {
      title: "Total Alerts",
      value: loading ? "..." : String(alerts.length).padStart(2, "0"),
      change: "Saved investigation alerts",
      icon: AlertTriangle,
      color: "orange",
    },
    {
      title: "Network Events",
      value: eventsLoading ? "..." : eventsError ? "N/A" : String(eventsTotal),
      change: eventsError
        ? "Event data unavailable"
        : !eventsLoading && eventsTotal === 0
          ? "No events recorded yet"
          : "Connections observed",
      icon: Network,
      color: "blue",
    },
    {
      title: "Open Alerts",
      value: loading ? "..." : String(openAlerts).padStart(2, "0"),
      change: "Awaiting review",
      icon: FileSearch,
      color: "purple",
    },
    {
      title: "API Status",
      value: statusBanner.card,
      change: "Backend connection",
      icon: ShieldCheck,
      color: "green",
    },
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Shield size={23} />
          </div>

          <div>
            <h2>
              CYBER<span>INVESTIGATOR</span>
            </h2>
            <p>Security Intelligence Platform</p>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>

        <nav className="navigation">
          <a className="nav-item active" href="#">
            <LayoutDashboard size={18} />
            Overview
          </a>

          <a className="nav-item" href="#">
            <Activity size={18} />
            Network Activity
          </a>

          <a className="nav-item" href="#">
            <AlertTriangle size={18} />
            Security Alerts
            <span className="nav-count">{alerts.length}</span>
          </a>

          <a className="nav-item" href="#">
            <FileSearch size={18} />
            Investigations
          </a>

          <a className="nav-item" href="#">
            <Network size={18} />
            Event Correlation
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="system-card">
            <div className="system-heading">
              <span className="status-dot"></span>
              Collector status
            </div>

            <p>Local monitoring is not connected yet.</p>
            <span className="system-tag">UI PREVIEW</span>
          </div>

          <a className="nav-item" href="#">
            <Settings size={18} />
            Settings
          </a>

          <div className="profile">
            <div className="avatar">CI</div>

            <div>
              <strong>Investigator</strong>
              <p>Local workspace</p>
            </div>

            <ChevronDown size={16} />
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <span>/</span> <strong>Overview</strong>
          </div>

          <div className="top-actions">
            <div className="search-box">
              <Search size={16} />
              <span>Search investigations...</span>
              <kbd>⌘ K</kbd>
            </div>

            <button className="icon-button" aria-label="Notifications">
              <Bell size={19} />
              <span className="notification-dot"></span>
            </button>

            <div className="user-avatar">CI</div>
          </div>
        </header>

        <section className="page-heading">
          <div>
            <div className="eyebrow">SECURITY OPERATIONS</div>

            <h1>Investigation Overview</h1>

            <p>
              Monitor activity, review alerts, and investigate suspicious events.
            </p>
          </div>

          <div className="date-label">
            <Clock size={15} />
            Local workspace
          </div>
        </section>

        <section className="status-banner">
          <div className="banner-icon">
            <Monitor size={21} />
          </div>

          <div>
            <strong>{statusBanner.title}</strong>

            <p>{statusBanner.message}</p>
          </div>

          <span className="preview-label">{statusBanner.label}</span>
        </section>

        <section className="stats-grid">
          {stats.map((item) => {
            const Icon = item.icon;

            return (
              <article className="stat-card" key={item.title}>
                <div className="stat-top">
                  <span>{item.title}</span>

                  <div className={`stat-icon ${item.color}`}>
                    <Icon size={19} />
                  </div>
                </div>

                <h2>{item.value}</h2>
                <p>{item.change}</p>
              </article>
            );
          })}
        </section>

        <section className="content-grid">
          <article className="panel activity-panel">
            <div className="panel-heading">
              <div>
                <h3>Network Activity</h3>
                <p>Connection monitoring overview</p>
              </div>

              <span className="panel-icon">
                <Activity size={18} />
              </span>
            </div>

            <div className="empty-chart">
              <div className="chart-decoration">
                <Activity size={34} />
              </div>

              <strong>Activity analytics coming next</strong>

              <p>
                We'll connect real network event data from the backend.
              </p>
            </div>
          </article>

          <article className="panel distribution-panel">
            <div className="panel-heading">
              <div>
                <h3>Investigation Summary</h3>
                <p>Current saved alert status</p>
              </div>

              <span className="panel-icon">
                <ShieldCheck size={18} />
              </span>
            </div>

            <div className="summary-number">
              {alerts.length.toString().padStart(2, "0")}
              <span> saved alerts</span>
            </div>

            <div className="summary-row">
              <span>
                <CircleDot size={12} />
                Open
              </span>
              <strong>{openAlerts}</strong>
            </div>

            <div className="summary-bar">
              <div
                className="summary-fill"
                style={{
                  width:
                    alerts.length > 0
                      ? `${(openAlerts / alerts.length) * 100}%`
                      : "0%",
                }}
              ></div>
            </div>

            <div className="summary-row muted">
              <span>Reviewed</span>
              <strong>{reviewedAlerts}</strong>
            </div>

            <div className="summary-row muted">
              <span>Closed</span>
              <strong>{closedAlerts}</strong>
            </div>
          </article>
        </section>

        <section className="panel alerts-panel">
          <div className="panel-heading">
            <div>
              <h3>Recent Security Alerts</h3>
              <p>Events saved for investigation</p>
            </div>

            <span className="view-all">
              {alerts.length} records
            </span>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ALERT</th>
                  <th>PROCESS</th>
                  <th>SEVERITY</th>
                  <th>TIME</th>
                  <th>STATUS</th>
                </tr>
              </thead>

              <tbody>
                {loading ? (
                  <tr>
                    <td colSpan="5">Loading alerts...</td>
                  </tr>
                ) : error ? (
                  <tr>
                    <td colSpan="5">{error}</td>
                  </tr>
                ) : alerts.length === 0 ? (
                  <tr>
                    <td colSpan="5">No saved alerts found.</td>
                  </tr>
                ) : (
                  alerts.map((alert) => (
                    <tr key={alert.alert_id}>
                      <td>
                        <strong>
                          {(alert.alert_type || "UNKNOWN").replaceAll("_", " ")}
                        </strong>
                      </td>

                      <td className="process-name">
                        {alert.process || "Unknown"}
                      </td>

                      <td>
                        <span
                          className={`severity ${(alert.severity || "low").toLowerCase()}`}
                        >
                          {alert.severity || "UNKNOWN"}
                        </span>
                      </td>

                      <td className="time-cell">
                        {alert.timestamp
                          ? new Date(alert.timestamp).toLocaleString()
                          : "Unknown"}
                      </td>

                      <td>
                        <span className="open-status">
                          {alert.status || "UNKNOWN"}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>

        <footer className="footer">
          <span>
            CYBER INVESTIGATOR
            <span className="footer-divider">/</span>
            DEFENSIVE SECURITY PLATFORM
          </span>

          <span>
            <Globe size={13} />
            Local environment
          </span>
        </footer>
      </main>
    </div>
  );
}

export default App;
