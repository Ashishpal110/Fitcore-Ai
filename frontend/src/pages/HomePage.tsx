import React from 'react';
import { Layers, ShieldCheck, Database, Cpu } from 'lucide-react';

export const HomePage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white">
          FitCore Foundation
        </h1>
        <p className="text-slate-400 mt-1">
          Phase 0: Project Foundation, Architecture &amp; Development Rules established.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/60 flex items-start gap-4">
          <div className="p-3 bg-sky-500/10 text-sky-400 rounded-lg">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-white">Layered Architecture</h3>
            <p className="text-sm text-slate-400 mt-1">
              Strict separation across API Routes, Pydantic Schemas, Service Layer, Repositories, and SQLAlchemy Models.
            </p>
          </div>
        </div>

        <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/60 flex items-start gap-4">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-lg">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-white">Data Isolation Principle</h3>
            <p className="text-sm text-slate-400 mt-1">
              Architecture guarantees multi-tenant security and zero cross-user data leakage across queries.
            </p>
          </div>
        </div>

        <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/60 flex items-start gap-4">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-lg">
            <Database className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-white">Multi-Modal Tracking Model</h3>
            <p className="text-sm text-slate-400 mt-1">
              Data architecture designed to support strength (weight+reps), bodyweight, cardio (distance+duration), and HIIT.
            </p>
          </div>
        </div>

        <div className="p-5 rounded-xl border border-slate-800 bg-slate-900/60 flex items-start gap-4">
          <div className="p-3 bg-amber-500/10 text-amber-400 rounded-lg">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h3 className="text-base font-semibold text-white">Modular Monolith</h3>
            <p className="text-sm text-slate-400 mt-1">
              Zero microservice overhead; robust FastAPI + React TypeScript ecosystem ready for Phase 1.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
