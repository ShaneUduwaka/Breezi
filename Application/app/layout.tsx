import './globals.css';
import type { Metadata } from 'next';
import { Providers } from './providers';
import { DashboardLayout } from '../components/DashboardLayout';

export const metadata: Metadata = {
  title: 'Breezi Dashboard',
  description: 'AI Call Agent Platform'
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <DashboardLayout>{children}</DashboardLayout>
        </Providers>
      </body>
    </html>
  );
}
