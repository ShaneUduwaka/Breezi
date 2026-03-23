'use client';

/**
 * LoadingSkeleton Component
 * Shows a skeleton loader while data is being fetched
 */

interface LoadingSkeletonProps {
  cardCount?: number;
}

export function LoadingSkeleton({ cardCount = 4 }: LoadingSkeletonProps) {
  return (
    <div className="space-y-4">
      {/* Header skeleton */}
      <div className="mb-6 space-y-2">
        <div className="h-8 w-32 animate-pulse rounded bg-slate-200" />
        <div className="h-5 w-64 animate-pulse rounded bg-slate-100" />
      </div>

      {/* Cards skeleton */}
      <div className="grid gap-4 grid-cols-1 md:grid-cols-2 xl:grid-cols-4">
        {Array.from({ length: cardCount }).map((_, i) => (
          <div key={i} className="card card-border p-5 space-y-2">
            <div className="h-4 w-20 animate-pulse rounded bg-slate-200" />
            <div className="h-8 w-16 animate-pulse rounded bg-slate-200" />
            <div className="h-4 w-24 animate-pulse rounded bg-slate-100" />
          </div>
        ))}
      </div>

      {/* Panel skeleton */}
      <div className="card card-border mt-6 space-y-3 p-5">
        <div className="h-6 w-40 animate-pulse rounded bg-slate-200" />
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="space-y-2">
            <div className="h-4 w-full animate-pulse rounded bg-slate-100" />
            <div className="h-4 w-3/4 animate-pulse rounded bg-slate-100" />
          </div>
        ))}
      </div>
    </div>
  );
}
