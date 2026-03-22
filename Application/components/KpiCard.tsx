'use client';

type KpiCardProps = {
  title: string;
  value: string;
  change: string;
  positive?: boolean;
};

export function KpiCard({ title, value, change, positive = true }: KpiCardProps) {
  return (
    <div className="card card-border p-5 bg-white">
      <div className="text-sm text-slate-500">{title}</div>
      <div className="mt-2 text-3xl font-semibold">{value}</div>
      <div className={`mt-1 text-sm font-medium ${positive ? 'text-emerald-500' : 'text-rose-500'}`}>
        {positive ? '▲' : '▼'} {change}
      </div>
    </div>
  );
}
