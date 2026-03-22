'use client';

import { useMemo } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { ProtectedRoute } from '../../../components/ProtectedRoute';
import { Sidebar } from '../../../components/Sidebar';
import { Topbar } from '../../../components/Topbar';
import { callLogs } from '../../../services/mockData';

export default function CallDetailsPage() {
  const params = useParams();
  const id = params?.id;

  const current = useMemo(() => callLogs.find((call) => call.id === id), [id]);

  if (!current) {
    return (
      <ProtectedRoute>
        <div className="p-10">Call record not found.</div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-white">
        <div className="flex">
          <Sidebar />
          <div className="flex-1 px-6 py-5">
            <Topbar />
            <div className="mt-5 mb-4">
              <Link href="/call-logs" className="text-sm text-breezi-500 hover:underline">
                ← Back to Call Logs
              </Link>
              <h1 className="text-3xl font-bold mt-2">Call {current.id}</h1>
              <p className="mt-1 text-slate-600">Detailed transcript, call metadata and status.</p>
            </div>

            <div className="grid gap-4 lg:grid-cols-3">
              <div className="lg:col-span-2 card card-border">
                <h3 className="text-xl font-semibold">Transcript</h3>
                <div className="mt-3 rounded-xl border border-slate-200 p-4 bg-white">
                  <p className="whitespace-pre-line text-sm leading-relaxed text-slate-700">{current.transcription.repeat(4)}</p>
                </div>

                <div className="mt-4 card card-border bg-white">
                  <h4 className="text-lg font-semibold">Audio Player</h4>
                  <audio controls className="mt-2 w-full rounded-lg border border-slate-300 p-2 bg-white">
                    Your browser does not support the audio element.
                  </audio>
                </div>
              </div>

              <div className="space-y-3">
                <div className="card card-border">
                  <h4 className="font-semibold">Call Metadata</h4>
                  <dl className="mt-2 text-sm text-slate-600">
                    <div className="flex justify-between py-1 border-b border-slate-100">
                      <dt>Caller</dt>
                      <dd>{current.caller}</dd>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-100">
                      <dt>Intent</dt>
                      <dd>{current.intent}</dd>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-100">
                      <dt>Duration</dt>
                      <dd>{current.duration} mins</dd>
                    </div>
                    <div className="flex justify-between py-1">
                      <dt>Status</dt>
                      <dd>{current.status}</dd>
                    </div>
                  </dl>
                </div>

                <div className="card card-border">
                  <h4 className="font-semibold">AI Status</h4>
                  <p className="mt-1 text-sm text-slate-600">This call has been processed by Breezi’s AI engine and scored as high quality.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
