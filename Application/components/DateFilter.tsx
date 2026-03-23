'use client';

import { Calendar } from 'lucide-react';
import { useDateStore, type DateRange } from '../store/dateStore';

const dateRangeOptions: { value: DateRange; label: string }[] = [
  { value: 'today', label: 'Today' },
  { value: 'last_7_days', label: 'Last 7 Days' },
  { value: 'this_month', label: 'This Month' },
  { value: 'all_time', label: 'All Time' },
];

export function DateFilter() {
  const { dateRange, setDateRange } = useDateStore();

  return (
    <div className="relative">
      <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-lg px-3 py-2 shadow-sm hover:border-gray-300 transition-colors">
        <Calendar className="h-4 w-4 text-gray-500" />
        <select
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value as DateRange)}
          className="bg-transparent border-none outline-none text-sm font-medium text-gray-700 cursor-pointer min-w-0"
        >
          {dateRangeOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}