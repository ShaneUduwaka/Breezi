import type { Metadata } from "next";
import { Geist, Geist_Mono, Inter, Poppins} from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const poppins = Poppins({
  subsets: ['latin'],
  weight: ['400', '600', '700'],
  variable: '--font-poppins',
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: 'Breezi AI - Unburden Your Staff, Elevate Service',
  description: 'Advanced AI Call Agent for seamless customer service and operational efficiency.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${poppins.variable}`}>
      <body className="bg-[#0A0A1F] text-gray-200 font-inter antialiased">
        {children}
      </body>
    </html>
  );
}
