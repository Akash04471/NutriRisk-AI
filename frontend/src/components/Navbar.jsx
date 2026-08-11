import React from 'react';
import { Activity, ShieldCheck, Cpu, AlertCircle } from 'lucide-react';

const Navbar = ({ activeTab, setActiveTab, apiStatus }) => {
  const isOnline = apiStatus && apiStatus.status === 'healthy';

  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200 custom-shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('home')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-500 flex items-center justify-center shadow-md shadow-emerald-500/20">
              <span className="text-xl">🥗</span>
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-extrabold text-xl tracking-tight text-slate-900 font-outfit">NutriRisk AI</span>
                <span className="px-2 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded-full">Ensemble ML</span>
              </div>
              <p className="text-xs text-slate-500 hidden sm:block">Explainable Nutritional Risk Prediction</p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex space-x-1">
            <button
              onClick={() => setActiveTab('home')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'home'
                  ? 'bg-emerald-50 text-emerald-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Overview
            </button>
            <button
              onClick={() => setActiveTab('assessment')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'assessment'
                  ? 'bg-emerald-50 text-emerald-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Risk Assessment
            </button>
            <button
              onClick={() => setActiveTab('metrics')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'metrics'
                  ? 'bg-emerald-50 text-emerald-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Model Performance
            </button>
            <button
              onClick={() => setActiveTab('ethics')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'ethics'
                  ? 'bg-emerald-50 text-emerald-700 font-semibold'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
              }`}
            >
              Responsible AI
            </button>
          </nav>

          {/* Backend API Status Pill */}
          <div className="flex items-center space-x-3">
            <div className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-full text-xs font-semibold border ${
              isOnline 
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200' 
                : 'bg-amber-50 text-amber-700 border-amber-200'
            }`}>
              <span className={`w-2 h-2 rounded-full ${isOnline ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`}></span>
              <span>{isOnline ? 'FastAPI Active' : 'Backend Connecting...'}</span>
            </div>

            <button
              onClick={() => setActiveTab('assessment')}
              className="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-lg text-sm font-semibold shadow-md shadow-emerald-600/20 transition-all hover:scale-105 active:scale-95"
            >
              Start Screening
            </button>
          </div>

        </div>
      </div>
    </header>
  );
};

export default Navbar;
