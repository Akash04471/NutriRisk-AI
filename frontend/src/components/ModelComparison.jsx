import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from 'recharts';
import { Cpu, Award } from 'lucide-react';

const ModelComparison = ({ modelInfo }) => {
  const metricsTable = modelInfo?.metrics_table || [
    { Model: 'Logistic Regression Baseline', 'CV ROC-AUC': 0.9982, 'Test ROC-AUC': 0.9996, Accuracy: 0.9904, Precision: 0.9864, Recall: 0.9932, 'F1-Score': 0.9898 },
    { Model: 'Random Forest (Bagging)', 'CV ROC-AUC': 1.0000, 'Test ROC-AUC': 1.0000, Accuracy: 1.0000, Precision: 1.0000, Recall: 1.0000, 'F1-Score': 1.0000 },
    { Model: 'XGBoost (Boosting)', 'CV ROC-AUC': 0.9999, 'Test ROC-AUC': 1.0000, Accuracy: 0.9968, Precision: 1.0000, Recall: 0.9932, 'F1-Score': 0.9966 },
    { Model: 'Stacking Ensemble', 'CV ROC-AUC': 1.0000, 'Test ROC-AUC': 1.0000, Accuracy: 0.9936, Precision: 0.9932, Recall: 0.9932, 'F1-Score': 0.9932 }
  ];

  return (
    <div className="space-y-8">
      {/* Architecture Highlights Banner */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 custom-shadow space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <div className="flex items-center space-x-2">
              <Cpu className="w-5 h-5 text-emerald-600" />
              <h3 className="text-xl font-bold text-slate-900 font-outfit">Ensemble Model Architecture (Q3 Rubric)</h3>
            </div>
            <p className="text-xs text-slate-600 mt-1">
              Evaluated under Stratified 5-Fold Cross Validation on untouched test data (15% split, random_state=42).
            </p>
          </div>

          <div className="flex items-center space-x-1 px-3 py-1.5 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold">
            <Award className="w-4 h-4" />
            <span>Best Model: Random Forest / Stacking</span>
          </div>
        </div>

        {/* Recharts Bar Chart */}
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={metricsTable} margin={{ top: 10, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="Model" tick={{ fontSize: 11, fill: '#475569' }} />
              <YAxis domain={[0.95, 1.01]} tick={{ fontSize: 11, fill: '#475569' }} />
              <Tooltip contentStyle={{ borderRadius: '12px', border: '1px solid #cbd5e1' }} />
              <Legend wrapperStyle={{ paddingTop: '10px', fontSize: '12px' }} />
              <Bar dataKey="CV ROC-AUC" fill="#0284c7" name="CV ROC-AUC" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Test ROC-AUC" fill="#059669" name="Test ROC-AUC" radius={[4, 4, 0, 0]} />
              <Bar dataKey="F1-Score" fill="#8b5cf6" name="F1-Score" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Recall" fill="#f59e0b" name="Recall" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Table of Exact Metrics */}
        <div className="overflow-x-auto pt-2">
          <table className="w-full text-xs text-left border-collapse">
            <thead>
              <tr className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                <th className="p-3 rounded-l-lg">Model Architecture</th>
                <th className="p-3">CV ROC-AUC</th>
                <th className="p-3">Test ROC-AUC</th>
                <th className="p-3">Precision</th>
                <th className="p-3">Recall</th>
                <th className="p-3 rounded-r-lg">F1-Score</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {metricsTable.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50 transition-all font-medium">
                  <td className="p-3 font-bold text-slate-900">{row.Model}</td>
                  <td className="p-3 text-slate-700">{row['CV ROC-AUC']?.toFixed(4)}</td>
                  <td className="p-3 font-bold text-emerald-700">{row['Test ROC-AUC']?.toFixed(4)}</td>
                  <td className="p-3 text-slate-700">{row.Precision?.toFixed(4)}</td>
                  <td className="p-3 font-bold text-amber-700">{row.Recall?.toFixed(4)}</td>
                  <td className="p-3 text-slate-700">{row['F1-Score']?.toFixed(4)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ModelComparison;
