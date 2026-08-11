import React from 'react';
import { Shield, Eye, Lock, AlertTriangle, UserCheck, FileText } from 'lucide-react';

const ResponsibleAI = () => {
  return (
    <div className="space-y-8">
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 custom-shadow space-y-6">
        <div className="flex items-center space-x-2 border-b border-slate-100 pb-4">
          <Shield className="w-6 h-6 text-purple-600" />
          <div>
            <h2 className="text-2xl font-bold text-slate-900 font-outfit">Ethics & Responsible AI (Q4 Rubric)</h2>
            <p className="text-xs text-slate-600">Addressing fairness, privacy, clinical cost trade-offs, and human oversight.</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Card 1: Educational Positioning */}
          <div className="p-5 rounded-2xl bg-amber-50/70 border border-amber-200/80 space-y-2">
            <div className="flex items-center space-x-2 font-bold text-amber-900 text-sm font-outfit">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Decision-Support Positioning</span>
            </div>
            <p className="text-xs text-amber-800 leading-relaxed">
              NutriRisk AI is an educational research prototype designed solely to assist dietitians and health workers during early screening. It does <strong>not diagnose medical conditions</strong> or prescribe clinical treatments.
            </p>
          </div>

          {/* Card 2: Privacy Protection */}
          <div className="p-5 rounded-2xl bg-emerald-50/70 border border-emerald-200/80 space-y-2">
            <div className="flex items-center space-x-2 font-bold text-emerald-900 text-sm font-outfit">
              <Lock className="w-4 h-4 text-emerald-600" />
              <span>Privacy & Data Protection</span>
            </div>
            <p className="text-xs text-emerald-800 leading-relaxed">
              The application does not collect, log, or store Personally Identifiable Information (PII) such as names, addresses, emails, or government medical IDs. Input payloads are processed in-memory during inference.
            </p>
          </div>

          {/* Card 3: Clinical FP vs FN Cost Analysis */}
          <div className="p-5 rounded-2xl bg-sky-50/70 border border-sky-200/80 space-y-2">
            <div className="flex items-center space-x-2 font-bold text-sky-900 text-sm font-outfit">
              <Eye className="w-4 h-4 text-sky-600" />
              <span>False Positive vs False Negative Costs</span>
            </div>
            <p className="text-xs text-sky-800 leading-relaxed">
              <strong>False Negative (High Clinical Cost):</strong> Missing an at-risk patient delays preventive care. Recall is prioritized.<br />
              <strong>False Positive (Low Clinical Cost):</strong> Recommending a low-risk patient for a routine consultation causes minimal harm.
            </p>
          </div>

          {/* Card 4: Human Oversight */}
          <div className="p-5 rounded-2xl bg-purple-50/70 border border-purple-200/80 space-y-2">
            <div className="flex items-center space-x-2 font-bold text-purple-900 text-sm font-outfit">
              <UserCheck className="w-4 h-4 text-purple-600" />
              <span>Human-in-the-Loop Oversight</span>
            </div>
            <p className="text-xs text-purple-800 leading-relaxed">
              Final screening decisions remain under human expert control. SHAP feature contribution charts provide clear rationale so practitioners understand the underlying drivers behind every probability score.
            </p>
          </div>
        </div>

        {/* Limitations Notice */}
        <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
          <h4 className="font-bold text-slate-900 text-sm font-outfit">Deployment Limitations</h4>
          <ul className="text-xs text-slate-600 space-y-1 list-disc list-inside leading-relaxed">
            <li>Dataset represents specific geographical cohorts (Colombia, Peru, Mexico); deployment in new populations requires local recalibration.</li>
            <li>Self-reported dietary and physical activity inputs are subject to recall bias and reporting inaccuracies.</li>
            <li>Model estimates represent statistical probabilities derived from historical data, not absolute medical certainty.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ResponsibleAI;
