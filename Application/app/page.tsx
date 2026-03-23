'use client';

import { useEffect, useState } from 'react';
import { KpiCard } from '../components/KpiCard';
import { LiveCallsPanel } from '../components/LiveCallsPanel';
import { LoadingSkeleton } from '../components/LoadingSkeleton';
import { fetchMetrics, fetchLiveCalls, type MetricsResponse, type LiveCall } from '../services/api';
import { useDateStore } from '../store/dateStore';

export default function DashboardPage() {
  const { dateRange } = useDateStore();
  const [workspace, setWorkspace] = useState('Acme Corp');
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [liveCalls, setLiveCalls] = useState<LiveCall[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Fetch both metrics and live calls in parallel
        const [metricsData, liveCallsData] = await Promise.all([
          fetchMetrics(dateRange),
          fetchLiveCalls(),
        ]);

        setMetrics(metricsData);
        setLiveCalls(liveCallsData);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load dashboard data';
        setError(message);
        console.error('Dashboard error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [dateRange]);

  if (isLoading) {
    return (
      <>
        <div className="mt-5 mb-6">
          <div className="mb-3 text-xs uppercase tracking-wide text-slate-500">{workspace}</div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="mt-2 text-slate-600">Your Breezi AI call insights in one place.</p>
        </div>
        <LoadingSkeleton cardCount={4} />
      </>
    );
  }

  if (error) {
    return (
      <>
        <div className="mt-5">
          <div className="mb-3 text-xs uppercase tracking-wide text-slate-500">{workspace}</div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
        </div>
        <div className="mt-6 rounded-lg border border-rose-200 bg-rose-50 p-4">
          <p className="text-sm font-medium text-rose-900">Error loading dashboard</p>
          <p className="mt-1 text-sm text-rose-700">{error}</p>
        </div>
      </>
    );
  }

  return (
    <>
      <div className="mt-5">
        <div className="mb-3 text-xs uppercase tracking-wide text-slate-500">{workspace}</div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="mt-2 text-slate-600">Your Breezi AI call insights in one place.</p>
      </div>

      {metrics && (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4 mt-6">
          <KpiCard title="Calls Today" value={`${metrics.callsToday}`} change={`${metrics.trend.callsToday}%`} />
          <KpiCard title="Total Minutes" value={`${metrics.totalMinutes} mins`} change={`${metrics.trend.totalMinutes}%`} />
          <KpiCard title="Success Rate" value={`${metrics.successRate}%`} change={`${metrics.trend.successRate}%`} />
          <KpiCard title="Active Agents" value={`${metrics.activeAgents}`} change={`${metrics.trend.activeAgents}%`} />
        </div>
      )}

      <div className="mt-6">
        <LiveCallsPanel calls={liveCalls} />
      </div>
    </>
  );
}
