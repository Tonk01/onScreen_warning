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

export default function Home() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [expandedAlertId, setExpandedAlertId] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/alerts")
    .then((response) => response.json())
    .then((data) => setAlerts(data));
  }, []);

  return (
      <main>
        <h1> OnScreen </h1>

        {alerts.map((alert) => {
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
                  <p>{alert.start_time}</p>
                  <p>{alert.end_time}</p>
                </div>
              )}
            </div>
          );
        })}
      </main>
  );
}
