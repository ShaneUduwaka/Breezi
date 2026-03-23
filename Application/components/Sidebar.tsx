'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { href: '/', label: 'Dashboard' },
  { href: '/call-logs', label: 'Call Logs' },
  { href: '/analytics', label: 'Analytics' },
  { href: '/settings', label: 'Settings' }
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="h-screen w-72 border-r border-slate-200 bg-white px-5 py-6 sticky top-0">
      <div className="font-bold text-2xl text-breezi-500 pb-8">Breezi</div>
      <div className="space-y-1">
        {navItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded-xl px-4 py-2 transition ${
                active
                  ? 'bg-breezi-500/15 text-breezi-500 font-semibold'
                  : 'text-slate-600 hover:bg-slate-100'
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </div>
    </aside>
  );
}
