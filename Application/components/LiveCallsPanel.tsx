'use client';

import type { LiveCall } from '../services/api';

interface LiveCallsPanelProps {
  calls?: LiveCall[];
}

export function LiveCallsPanel({ calls = [] }: LiveCallsPanelProps) {
  if (calls.length === 0) {
    return (
      <div className="card card-border">
        <h3 className="text-xl font-semibold mb-3">Live Call Monitoring</h3>
        <p className="text-sm text-slate-500">No active calls at the moment.</p>
      </div>
    );
  }

  return (
    <div className="card card-border">
      <h3 className="text-xl font-semibold mb-3">Live Call Monitoring</h3>
      <div className="space-y-3">
        {calls.map((call) => (
          <div key={call.id} className="rounded-xl border border-slate-200 p-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold">{call.caller} ({call.intent})</p>
                <p className="text-sm text-slate-500">Agent: {call.agent}</p>
              </div>
              <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-700">LIVE</span>
            </div>
            <p className="mt-2 text-sm text-slate-500">Duration: {call.duration}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
