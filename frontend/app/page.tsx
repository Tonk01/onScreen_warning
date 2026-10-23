"use client";

import { useEffect, useState } from "react";
import { Alert } from "@/types/alert";

function getAffectedLines(alert: Alert): String[] {
  if (alert.affects.lines.length > 0) {
    return alert.affects.lines.map((line) => line.split(":").pop())
    .filter((line): line is string => Boolean (line));
  }

  return alert.affects.journeys.map((journey) => {
    const journeyId = journey.split(":").pop();

    if (!journeyId) {
      return null;
    }
    return journeyId.split("-")[0];
  }).filter((line): line is string => Boolean(line))
}

function formatDateTime(value: string | null): string {
  if (!value) {
    return "N/A";
  }

  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(new Date(value));
}

export default function Home() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [expandedAlertId, setExpandedAlertId] = useState<string | null>(null);
  const [view, setView]  = useState<"active" | "dismissed">("active");
  const [dismissedAlertIds, setDismissedAlerts] = useState<string[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/alerts")
    .then((response) => response.json())
    .then((data) => setAlerts(data));
  }, []);

  function dismissAlerts(alertId: string) {
    setDismissedAlerts((current) => [...current, alertId]);
    setExpandedAlertId(null);
  }

  function restoreAlert(alertId: string) {
    setDismissedAlerts((current) => current.filter((id) => id !== alertId));
    setExpandedAlertId(null);
  }

  const activeAlerts = alerts.filter((alert) => !dismissedAlertIds.includes(alert.id));
  const dismissedAlerts = alerts.filter((alert) => dismissedAlertIds.includes(alert.id));

  const displayedAlerts = view === "active" ? activeAlerts : dismissedAlerts;

  return (
      <main>
        <h1> OnScreen </h1>

        <div className="view-switcher">
          <button onClick={() => setView("active")}>
            Active alerts
          </button>

          <button onClick={() => setView("dismissed")}>
            Dismissed alerts
          </button>
        </div>

        {displayedAlerts.map((alert) => {
          const lines = [...new Set(getAffectedLines(alert))];
          const message = alert.description || alert.summary;
          const isExpanded = expandedAlertId === alert.id;

          return (
            <div className = "alert-card" key = {alert.id} onClick={() => setExpandedAlertId(isExpanded ? null : alert.id)}>
              {lines.length > 0 && (
                <p className = "alert-lines">
                  {lines.length == 1 ? "Linje " : "Linjer "}
                  {lines.join(", ")}
                </p>
              )}
              <h2 className = "alert-summary"> {message} </h2>

              {isExpanded && (
                <div className="alert-details">
                  <p>{alert.summary}</p>
                  <h3> {formatDateTime(alert.start_time)} ー {formatDateTime(alert.end_time)} </h3>

                  {view === "active" ? (
                    <button onClick = {(event) => {
                      event.stopPropagation();
                      dismissAlerts(alert.id);
                    }}
                    >
                      Dismiss alert
                    </button>
                  ) : (
                    <button onClick = {(event) => {
                      event.stopPropagation();
                      restoreAlert(alert.id);
                  }}
                  >
                    Activate alert
                    </button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </main>
  );
}
