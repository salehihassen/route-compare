import { Header } from './Header';

interface MainLayoutProps {
  children: React.ReactNode;
}

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-background font-sans antialiased">
      <Header />
      <main className="container py-8">
        {children}
      </main>
    </div>
  );
}
