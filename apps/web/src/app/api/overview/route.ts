import { NextResponse } from 'next/server';
import { overviewMetricsSchema } from '@/lib/overview-metrics';

const metrics = [
  { label: 'MRR', value: '$42,800', delta: '+6.2%' },
  { label: 'Active Accounts', value: '1,284', delta: '+3.1%' },
  { label: 'Churn', value: '1.4%', delta: '-0.3%' }
];

export async function GET() {
  const parsed = overviewMetricsSchema.parse(metrics);
  return NextResponse.json({ metrics: parsed });
}
