'use client';

import { ReactNode } from 'react';
import { usePathname } from 'next/navigation';
import { AuthGuard } from '../components/AuthGuard';
import { Sidebar } from '../components/Sidebar';
import { Topbar } from '../components/Topbar';

interface DashboardLayoutProps {
  children: ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const isLoginPage = pathname === '/login';

  // For login page, just render children without layout
  if (isLoginPage) {
    return <>{children}</>;
  }

  // For all other pages, wrap with AuthGuard and dashboard layout
  return (
    <AuthGuard>
      <div className="min-h-screen bg-white">
        <div className="flex">
          <Sidebar />
          <div className="flex-1">
            <Topbar />
            <main className="px-6 py-5">
              {children}
            </main>
          </div>
        </div>
      </div>
    </AuthGuard>
  );
}