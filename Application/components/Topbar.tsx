'use client';

import { useRouter } from 'next/navigation';
import { useAuthStore } from '../store/authStore';
import { DateFilter } from './DateFilter';

const businesses = [
  { id: 'acme', name: 'Acme Corp' },
  { id: 'solace', name: 'Solace Ltd.' },
  { id: 'nova', name: 'Nova Group' }
];

export function Topbar({ onSwitch }: { onSwitch?: (business: string) => void }) {
  const { user, logout } = useAuthStore();
  const router = useRouter();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Get user initials
  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(word => word.charAt(0).toUpperCase())
      .join('')
      .slice(0, 2);
  };

  return (
    <div className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">
      <div className="flex items-center gap-3">
        <span className="text-xs uppercase tracking-wide font-semibold text-slate-500">Workspace</span>
        <select
          defaultValue={businesses[0].id}
          onChange={(e) => onSwitch?.(e.target.value)}
          className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none transition hover:border-breezi-500 focus:border-breezi-500"
        >
          {businesses.map((biz) => (
            <option key={biz.id} value={biz.id}>
              {biz.name}
            </option>
          ))}
        </select>
      </div>
      <div className="flex items-center gap-4">
        <DateFilter />
        <button
          onClick={handleLogout}
          className="rounded-lg border border-slate-300 px-3 py-2 text-sm hover:border-breezi-500 transition-colors"
        >
          Logout
        </button>
        <div className="rounded-full bg-slate-100 px-3 py-2 text-sm font-medium">
          {user ? getInitials(user.name) : 'U'}
        </div>
      </div>
    </div>
  );
}
