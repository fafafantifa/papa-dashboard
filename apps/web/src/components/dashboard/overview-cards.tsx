const cards = [
  { label: 'MRR', value: '$42,800', delta: '+6.2%' },
  { label: 'Active Accounts', value: '1,284', delta: '+3.1%' },
  { label: 'Churn', value: '1.4%', delta: '-0.3%' }
];

export function OverviewCards() {
  return (
    <section style={{ display: 'grid', gap: 12, gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))' }}>
      {cards.map((card) => (
        <article
          key={card.label}
          style={{
            borderRadius: 12,
            border: '1px solid #e2e8f0',
            background: '#fff',
            padding: 16
          }}
        >
          <p style={{ margin: 0, fontSize: 12, color: '#475569' }}>{card.label}</p>
          <p style={{ margin: '8px 0', fontSize: 24, fontWeight: 700 }}>{card.value}</p>
          <p style={{ margin: 0, fontSize: 13, color: '#16a34a' }}>{card.delta} vs last month</p>
        </article>
      ))}
    </section>
  );
}
