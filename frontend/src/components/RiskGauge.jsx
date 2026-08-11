import React from 'react';

const RiskGauge = ({ probability }) => {
  const percentage = Math.round(probability * 100);

  return (
    <div className="space-y-3">
      <div className="flex justify-between items-center text-xs font-bold text-slate-700">
        <span className="text-emerald-700">LOW (0%)</span>
        <span className="text-amber-700">MODERATE (35%)</span>
        <span className="text-rose-700">HIGH (65%+)</span>
      </div>

      {/* Progress Track */}
      <div className="relative w-full h-4 bg-slate-200 rounded-full overflow-hidden p-0.5 border border-slate-300/80">
        <div 
          className="h-full rounded-full transition-all duration-1000 bg-gradient-to-r from-emerald-500 via-amber-500 to-rose-600 shadow-sm"
          style={{ width: `${percentage}%` }}
        />
      </div>

      <div className="flex justify-between text-xs text-slate-500">
        <span>0.0</span>
        <span className="font-bold text-slate-900 text-sm">{percentage}% Probability</span>
        <span>1.0</span>
      </div>
    </div>
  );
};

export default RiskGauge;
