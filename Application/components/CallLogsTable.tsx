'use client';

import { useMemo, useState } from 'react';
import { CallRecord } from '../services/mockData';

type Props = {
  data: CallRecord[];
  onRowClick: (item: CallRecord) => void;
};

export function CallLogsTable({ data, onRowClick }: Props) {
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const pageSize = 10;

  const filtered = useMemo(() => {
    const normalize = (text: string) => text.toLowerCase();
    return data.filter((call) => {
      return (
        normalize(call.id).includes(normalize(search)) ||
        normalize(call.caller).includes(normalize(search)) ||
        normalize(call.intent).includes(normalize(search)) ||
        normalize(call.status).includes(normalize(search))
      );
    });
  }, [data, search]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / pageSize));
  const pageData = filtered.slice((page - 1) * pageSize, page * pageSize);

  return (
    <div className="card card-border">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 mb-4">
        <h3 className="text-xl font-semibold">Call Logs</h3>
        <input
          type="text"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setPage(1);
          }}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 outline-none focus:ring-2 focus:ring-breezi-200"
          placeholder="Search by call id, caller, intent or status"
        />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full min-w-[720px] table-auto text-left border-collapse">
          <thead className="text-slate-600 text-sm">
            <tr>
              <th className="px-4 py-3">Call ID</th>
              <th className="px-4 py-3">Caller</th>
              <th className="px-4 py-3">Intent</th>
              <th className="px-4 py-3">Duration</th>
              <th className="px-4 py-3">Time</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {pageData.map((row) => (
              <tr
                key={row.id}
                onClick={() => onRowClick(row)}
                className="cursor-pointer transition hover:bg-slate-100"
              >
                <td className="px-4 py-3">{row.id}</td>
                <td className="px-4 py-3">{row.caller}</td>
                <td className="px-4 py-3">{row.intent}</td>
                <td className="px-4 py-3">{row.duration}m</td>
                <td className="px-4 py-3">{row.time}</td>
                <td className="px-4 py-3">
                  <span
                    className={`rounded-full px-2 py-1 text-xs font-semibold ${
                      row.status === 'Completed'
                        ? 'bg-emerald-100 text-emerald-700'
                        : row.status === 'Transferred'
                        ? 'bg-indigo-100 text-indigo-700'
                        : row.status === 'Missed'
                        ? 'bg-rose-100 text-rose-700'
                        : 'bg-slate-100 text-slate-700'
                    }`}
                  >
                    {row.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-center justify-between text-sm">
        <span>
          Showing {pageData.length} of {filtered.length} calls
        </span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="rounded-lg border px-3 py-1 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Prev
          </button>
          <span>
            {page}/{totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="rounded-lg border px-3 py-1 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
