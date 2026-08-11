import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { HelpCircle, TrendingUp, TrendingDown } from 'lucide-react';

const ShapExplanation = ({ explanation }) => {
  if (!explanation || (!explanation.positive?.length && !explanation.negative?.length)) {
    return null;
  }

  const { positive = [], negative = [] } = explanation;

  // Prepare data for Recharts horizontal bar chart
  const chartData = [
    ...positive.map((f) => ({
      name: f.displayName,
      contribution: f.contribution,
      value: f.value,
      direction: 'positive',
    })),
    ...negative.map((f) => ({
      name: f.displayName,
      contribution: f.contribution,
      value: f.value,
      direction: 'negative',
    })),
  ].sort((a, b) => Math.abs(b.contribution) - Math.abs(a.contribution));

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 custom-shadow space-y-6">
      <div className="flex items-center justify-between border-b border-slate-100 pb-4">
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="text-xl font-bold text-slate-900 font-outfit">Why Did the Model Make This Prediction?</h3>
            <span className="px-2.5 py-0.5 text-xs font-semibold bg-teal-100 text-teal-800 rounded-full">SHAP Interpretability</span>
          </div>
          <p className="text-xs text-slate-600 mt-1">
            Game-theoretic feature attribution showing key individual factors driving the prediction score.
          </p>
        </div>
      </div>

      {/* Recharts Bar Chart */}
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            layout="vertical"
            data={chartData}
            margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
          >
            <XAxis type="number" domain={['dataMin - 0.05', 'dataMax + 0.05']} tick={{ fontSize: 11 }} />
            <YAxis type="category" dataKey="name" width={140} tick={{ fontSize: 11, fill: '#334155' }} />
            <Tooltip
              formatter={(val, name, props) => [`${val > 0 ? '+' : ''}${val}`, 'SHAP Contribution']}
              contentStyle={{ borderRadius: '12px', border: '1px solid #cbd5e1', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
            />
            <ReferenceLine x={0} stroke="#94a3b8" strokeDasharray="3 3" />
            <Bar dataKey="contribution" radius={[0, 4, 4, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.contribution > 0 ? '#f43f5e' : '#10b981'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Factor Breakdown Lists */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-2">
        
        {/* Factors Increasing Risk */}
        <div className="p-4 rounded-2xl bg-rose-50/60 border border-rose-200/80 space-y-3">
          <div className="flex items-center space-x-2 text-rose-900 font-bold text-sm font-outfit">
            <TrendingUp className="w-4 h-4 text-rose-600" />
            <span>Factors Increasing Risk</span>
          </div>

          <div className="space-y-2">
            {positive.length > 0 ? (
              positive.map((factor, idx) => (
                <div key={idx} className="flex justify-between items-center bg-white p-2.5 rounded-xl border border-rose-100 text-xs">
                  <div>
                    <span className="font-semibold text-slate-900">{factor.displayName}</span>
                    <span className="text-slate-500 text-[11px] block">Val: {factor.value}</span>
                  </div>
                  <span className="font-extrabold text-rose-600 bg-rose-50 px-2 py-1 rounded-lg">
                    +{factor.contribution}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 italic">No strong positive risk factors detected.</p>
            )}
          </div>
        </div>

        {/* Factors Reducing Risk */}
        <div className="p-4 rounded-2xl bg-emerald-50/60 border border-emerald-200/80 space-y-3">
          <div className="flex items-center space-x-2 text-emerald-900 font-bold text-sm font-outfit">
            <TrendingDown className="w-4 h-4 text-emerald-600" />
            <span>Factors Reducing Risk</span>
          </div>

          <div className="space-y-2">
            {negative.length > 0 ? (
              negative.map((factor, idx) => (
                <div key={idx} className="flex justify-between items-center bg-white p-2.5 rounded-xl border border-emerald-100 text-xs">
                  <div>
                    <span className="font-semibold text-slate-900">{factor.displayName}</span>
                    <span className="text-slate-500 text-[11px] block">Val: {factor.value}</span>
                  </div>
                  <span className="font-extrabold text-emerald-600 bg-emerald-50 px-2 py-1 rounded-lg">
                    {factor.contribution}
                  </span>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-500 italic">No strong negative risk factors detected.</p>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default ShapExplanation;
