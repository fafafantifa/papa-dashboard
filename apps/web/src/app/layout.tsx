import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'Papa Dashboard',
  description: 'Starter dashboard scaffold'
};

type RootLayoutProps = {
  children: ReactNode;
};

export function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

export default RootLayout;
