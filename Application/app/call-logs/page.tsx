'use client';

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { CallLogsTable } from '../../components/CallLogsTable';
import { fetchCallLogs } from '../../services/api';
import { useDateStore } from '../../store/dateStore';
import { type CallRecord } from '../../services/mockData';

export default function CallLogsPage() {
  const { dateRange } = useDateStore();
  const [callLogsData, setCallLogsData] = useState<{ data: CallRecord[]; total: number } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [workspace, setWorkspace] = useState('Acme Corp');

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await fetchCallLogs({ dateRange });
        setCallLogsData(data);
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load call logs';
        setError(message);
        console.error('Call logs fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [dateRange]);

  const callLogs = callLogsData?.data || [];
  const recent = useMemo(() => callLogs.slice(0, 5), [callLogs]);

  if (isLoading) {
    return (
      <>
        <div className="mt-5 mb-4">
          <div className="text-xs uppercase tracking-wide text-slate-500">{workspace}</div>
          <h1 className="text-3xl font-bold">Call Logs</h1>
          <p className="mt-1 text-slate-600">All calls details, history and status.</p>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="space-y-3">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="h-16 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-6 bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <div className="animate-pulse">
            <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="space-y-3">
              {Array.from({ length: 3 }).map((_, i) => (
                <div key={i} className="h-12 bg-gray-200 rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </>
    );
  }

  if (error) {
    return (
      <>
        <div className="mt-5 mb-4">
          <div className="text-xs uppercase tracking-wide text-slate-500">{workspace}</div>
          <h1 className="text-3xl font-bold">Call Logs</h1>
          <p className="mt-1 text-slate-600">All calls details, history and status.</p>
        </div>

        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <div className="text-center py-12">
            <p className="text-red-600 font-medium">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <div className="mt-5 mb-4">
        <div className="text-xs uppercase tracking-wide text-slate-500">{workspace}</div>
        <h1 className="text-3xl font-bold">Call Logs</h1>
        <p className="mt-1 text-slate-600">All calls details, history and status.</p>
      </div>

      <CallLogsTable data={callLogs} onRowClick={(record) => {}} />

      <div className="mt-6 card card-border">
        <h3 className="text-xl font-semibold">Recent Calls</h3>
        <ul className="mt-3 space-y-2">
          {recent.map((row) => (
            <li key={row.id} className="rounded-lg border border-slate-200 p-3">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-semibold">{row.id} - {row.caller}</p>
                  <p className="text-sm text-slate-500">{row.intent} • {row.status}</p>
                </div>
                <Link href={`/call-logs/${row.id}`} className="text-breezi-500 hover:text-breezi-700 text-sm">
                  View details
                </Link>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}
