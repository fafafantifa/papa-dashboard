import { OverviewCards } from '@/components/dashboard/overview-cards';

export default function OverviewPage() {
  return (
    <main style={{ maxWidth: 960, margin: '0 auto', padding: 24 }}>
      <header style={{ marginBottom: 20 }}>
        <h1 style={{ margin: '0 0 8px 0' }}>Overview</h1>
        <p style={{ margin: 0, color: '#475569' }}>Initial vertical slice scaffold for high-level KPIs.</p>
      </header>

      <OverviewCards />
    </main>
  );
}
