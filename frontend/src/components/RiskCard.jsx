import React from 'react';
import RiskGauge from './RiskGauge';
import { AlertTriangle, CheckCircle, Info, Activity } from 'lucide-react';

const RiskCard = ({ result }) => {
  if (!result) return null;

  const { risk_class, risk_label, probability, bmi, dietary_quality_index, model_name } = result;

  const isHigh = risk_class === 'High';
  const isMod = risk_class === 'Moderate';

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 custom-shadow space-y-6">
      <div className="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Screening Risk Result</span>
          <h3 className="text-2xl font-extrabold text-slate-900 font-outfit">Your Nutritional Risk</h3>
        </div>
        <span className="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full">
          Engine: {model_name || 'Stacking Ensemble'}
        </span>
      </div>

      {/* Risk Badge */}
      <div className={`p-5 rounded-2xl border text-center space-y-2 ${
        isHigh 
          ? 'bg-rose-50 border-rose-200 text-rose-900' 
          : isMod 
          ? 'bg-amber-50 border-amber-200 text-amber-900' 
          : 'bg-emerald-50 border-emerald-200 text-emerald-900'
      }`}>
        <div className="flex items-center justify-center space-x-2">
          {isHigh ? (
            <AlertTriangle className="w-6 h-6 text-rose-600" />
          ) : isMod ? (
            <Info className="w-6 h-6 text-amber-600" />
          ) : (
            <CheckCircle className="w-6 h-6 text-emerald-600" />
          )}
          <span className="text-2xl font-black font-outfit uppercase tracking-wide">
            {risk_class} NUTRITIONAL RISK
          </span>
        </div>
        <p className="text-sm font-medium opacity-90">{risk_label}</p>
      </div>

      {/* Risk Probability Gauge */}
      <div className="space-y-2 pt-2">
        <span className="text-xs font-bold text-slate-700">Estimated Risk Probability</span>
        <RiskGauge probability={probability} />
      </div>

      {/* Calculated Clinical Indicators */}
      <div className="grid grid-cols-2 gap-4 pt-2">
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
          <div className="text-xs font-semibold text-slate-500">Calculated BMI</div>
          <div className="text-xl font-black text-slate-900 font-outfit mt-1">{bmi} <span className="text-xs text-slate-500 font-normal">kg/m²</span></div>
          <div className="text-[11px] text-slate-500 mt-0.5">
            {bmi < 18.5 ? 'Underweight' : bmi < 25 ? 'Normal' : bmi < 30 ? 'Overweight' : 'Obesity Range'}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80">
          <div className="text-xs font-semibold text-slate-500">Dietary Quality Index</div>
          <div className="text-xl font-black text-emerald-700 font-outfit mt-1">{dietary_quality_index} <span className="text-xs text-slate-500 font-normal">/ 6.0</span></div>
          <div className="text-[11px] text-slate-500 mt-0.5">Veg & Water vs Caloric Density</div>
        </div>
      </div>

      {/* Recommendation Notice */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-700 leading-relaxed flex items-start space-x-2">
        <Activity className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
        <div>
          <strong>Clinical Decision Support Note:</strong>{' '}
          {isHigh
            ? 'The model estimates an elevated nutritional risk. Recommended for professional dietary assessment and lifestyle intervention.'
            : isMod
            ? 'Moderate nutritional risk detected. Recommend monitoring daily vegetable/water intake and increasing exercise.'
            : 'Low nutritional risk estimated. Maintain current balanced diet and regular physical activity.'}
        </div>
      </div>
    </div>
  );
};

export default RiskCard;
