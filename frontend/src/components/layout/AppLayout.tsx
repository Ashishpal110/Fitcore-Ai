import React from 'react';
import { Outlet } from 'react-router-dom';
import { Activity, Dumbbell, Calendar, TrendingUp, Settings } from 'lucide-react';

export const AppLayout: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-slate-950 text-slate-100">
      {/* Desktop Sidebar Shell */}
      <aside className="hidden md:flex flex-col w-64 border-r border-slate-800 bg-slate-900/50 p-4">
        <div className="flex items-center gap-3 px-2 py-4 mb-6">
          <Activity className="w-7 h-7 text-sky-500" />
          <span className="font-bold text-xl tracking-tight">FitCore</span>
        </div>

        <nav className="flex-1 space-y-1">
          <div className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg text-slate-400 cursor-not-allowed">
            <Dumbbell className="w-5 h-5" />
            <span>Workouts (Phase 5)</span>
          </div>
          <div className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg text-slate-400 cursor-not-allowed">
            <Calendar className="w-5 h-5" />
            <span>History (Phase 5)</span>
          </div>
          <div className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg text-slate-400 cursor-not-allowed">
            <TrendingUp className="w-5 h-5" />
            <span>Analytics (Phase 7)</span>
          </div>
        </nav>

        <div className="pt-4 border-t border-slate-800">
          <div className="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-lg text-slate-400 cursor-not-allowed">
            <Settings className="w-5 h-5" />
            <span>Settings</span>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Mobile Header Shell */}
        <header className="md:hidden flex items-center justify-between p-4 border-b border-slate-800 bg-slate-900/50">
          <div className="flex items-center gap-2">
            <Activity className="w-6 h-6 text-sky-500" />
            <span className="font-bold text-lg tracking-tight">FitCore</span>
          </div>
          <span className="text-xs px-2 py-1 bg-sky-500/10 text-sky-400 border border-sky-500/20 rounded-full font-mono">
            v1.0 Foundation
          </span>
        </header>

        {/* Dynamic Page Outlet */}
        <div className="flex-1 p-4 md:p-8 max-w-7xl w-full mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
};
