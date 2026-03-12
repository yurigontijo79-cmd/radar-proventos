import { useEffect, useState } from "react";

import { api } from "../api";

const cardStyle = {
  border: "1px solid #ddd",
  borderRadius: 8,
  padding: 16,
  minWidth: 180,
};

export default function Dashboard() {
  const [summary, setSummary] = useState({ events: 0, holdings: 0 });
  const [events, setEvents] = useState([]);
  const [holdings, setHoldings] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [summaryData, upcomingData, holdingsData] = await Promise.all([
          api.summary(),
          api.upcomingEvents(),
          api.holdings(),
        ]);
        setSummary(summaryData);
        setEvents(upcomingData);
        setHoldings(holdingsData);
      } catch (err) {
        setError(`Falha ao carregar dashboard: ${err.message}`);
      }
    }

    load();
  }, []);

  return (
    <main style={{ fontFamily: "Arial, sans-serif", padding: 24 }}>
      <h1>Radar de Proventos</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <section style={{ display: "flex", gap: 16, marginBottom: 24 }}>
        <div style={cardStyle}>
          <strong>Eventos</strong>
          <p>{summary.events}</p>
        </div>
        <div style={cardStyle}>
          <strong>Holdings</strong>
          <p>{summary.holdings}</p>
        </div>
      </section>

      <section style={{ marginBottom: 24 }}>
        <h2>Próximos eventos</h2>
        <ul>
          {events.map((event) => (
            <li key={event.id}>
              {event.ticker} · {event.event_type} · R$ {event.amount_per_share.toFixed(2)} · pagamento {event.payment_date || "-"}
            </li>
          ))}
          {events.length === 0 && <li>Sem eventos futuros.</li>}
        </ul>
      </section>

      <section>
        <h2>Carteira</h2>
        <ul>
          {holdings.map((holding) => (
            <li key={holding.id}>
              {holding.ticker} · {holding.quantity} ações
            </li>
          ))}
          {holdings.length === 0 && <li>Sem holdings cadastradas.</li>}
        </ul>
      </section>
    </main>
  );
}
