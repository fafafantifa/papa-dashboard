import { z } from 'zod';

export const overviewMetricSchema = z.object({
  label: z.string(),
  value: z.string(),
  delta: z.string()
});

export const overviewMetricsSchema = z.array(overviewMetricSchema);

export type OverviewMetric = z.infer<typeof overviewMetricSchema>;
