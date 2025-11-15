'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import { LayoutDashboard, FileText, Upload, BarChart3 } from 'lucide-react';

const navItems = [
  {
    title: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    title: 'Reports',
    href: '/reports',
    icon: FileText,
  },
  {
    title: 'Upload',
    href: '/dashboard?upload=true',
    icon: Upload,
  },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="hidden md:flex md:w-64 md:flex-col md:fixed md:left-0 md:top-16 md:bottom-0 md:z-40 md:border-r md:bg-background">
      <div className="flex flex-col flex-1 overflow-y-auto pt-6 pb-4">
        <nav className="flex-1 px-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href.includes('/dashboard') && pathname.startsWith('/dashboard'));
            
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  'group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors',
                  isActive
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                )}
              >
                <Icon
                  className={cn(
                    'mr-3 h-5 w-5 flex-shrink-0',
                    isActive ? 'text-primary' : 'text-muted-foreground group-hover:text-accent-foreground'
                  )}
                />
                {item.title}
              </Link>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
