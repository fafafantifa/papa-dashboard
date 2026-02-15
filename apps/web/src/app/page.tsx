import Link from 'next/link';

export default function HomePage() {
  return (
    <main style={{ padding: 24 }}>
      <h1>Papa Dashboard</h1>
      <p>Starter workspace is ready.</p>
      <Link href="/overview">Go to Overview →</Link>
    </main>
  );
}
