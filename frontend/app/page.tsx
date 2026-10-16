"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [alerts, setAlerts] = useState([])


  useEffect(() => {
    fetch("http://127.0.0.1:8000/alerts")
    .then((response) => response.json())
    .then((data) => setAlerts(data));
  }, []);

  return (
      <main>
        <h1> OnScreen </h1>

        <pre> {JSON.stringify(alerts, null, 2)} </pre>
      </main>
  );
}
