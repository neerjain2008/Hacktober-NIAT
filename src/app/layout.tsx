import type { Metadata } from 'next';
import { Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
});

export const metadata: Metadata = {
  title: 'ScamShield OSS | Privacy-First Open Source Scam Intelligence',
  description:
    'High-speed deterministic scam detection engine with URL heuristics, in-browser WebAssembly OCR, and 100% on-device AI threat synthesis with zero cloud transmission.',
  keywords: [
    'scam detection',
    'cybersecurity',
    'phishing detector',
    'smishing',
    'fraud intelligence',
    'open source',
    'privacy-first',
    'zero-log',
    'fastapi',
    'ollama',
    'gemma',
  ],
  authors: [{ name: 'ScamShield OSS Community' }],
  metadataBase: new URL('https://scamshield.dev'),
  openGraph: {
    title: 'ScamShield OSS | Open Source Scam Intelligence Engine',
    description:
      'Detect smishing, phishing URLs, advance-fee frauds, and chat scams in real time with 0ms deterministic heuristics and 100% on-device AI.',
    url: 'https://scamshield.dev',
    siteName: 'ScamShield OSS',
    images: [
      {
        url: '/brand-banner.jpg',
        width: 1200,
        height: 630,
        alt: 'ScamShield OSS Banner',
      },
    ],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'ScamShield OSS | Privacy-First Scam Intelligence Engine',
    description:
      'Zero-database, client-first cyber fraud intelligence platform powered by deterministic heuristics and local AI.',
    images: ['/brand-banner.jpg'],
  },
  icons: {
    icon: '/scamshield-icon.png',
    apple: '/scamshield-icon.png',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable} dark`}>
      <body className="min-h-screen bg-[#050505] text-slate-100 font-sans selection:bg-white/20 selection:text-white">
        {children}
      </body>
    </html>
  );
}
