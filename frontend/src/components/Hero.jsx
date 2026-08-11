import React from 'react';
import { ArrowRight, Cpu, Layers, Shield, FileCheck, CheckCircle2 } from 'lucide-react';

const Hero = ({ onStart }) => {
  return (
    <div className="space-y-16 pb-12">
      {/* Hero Banner Section */}
      <section className="relative overflow-hidden pt-12 pb-16 gradient-bg rounded-3xl border border-emerald-100/80 custom-shadow">
        <div className="max-w-4xl mx-auto text-center px-4 space-y-6">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-emerald-100/80 border border-emerald-200 text-emerald-800 text-xs font-semibold">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500"></span>
            <span>MCA 521-4 Machine Learning Assessment Project</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 font-outfit leading-tight">
            Explainable <span className="gradient-text">Nutritional Risk</span> Prediction
          </h1>

          <p className="text-lg sm:text-xl text-slate-600 font-normal max-w-2xl mx-auto leading-relaxed">
            Understand the physical, dietary, and lifestyle factors that influence individual nutritional risk using heterogeneous ensemble machine learning.
          </p>

          <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              onClick={onStart}
              className="w-full sm:w-auto bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-base px-8 py-3.5 rounded-xl shadow-lg shadow-emerald-600/30 transition-all hover:scale-[1.02] active:scale-95 flex items-center justify-center space-x-2"
            >
              <span>Analyze Nutritional Risk</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>

          {/* Academic Disclaimer */}
          <div className="pt-6 border-t border-slate-200/60 max-w-xl mx-auto">
            <p className="text-xs text-slate-500 italic">
              <strong>Disclaimer:</strong> NutriRisk AI is an educational/research decision-support prototype and is not a medical diagnostic system. Predictions should not replace professional nutritional or medical advice.
            </p>
          </div>
        </div>
      </section>

      {/* Model Highlights Cards */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="p-6 rounded-2xl bg-white border border-slate-200 custom-shadow space-y-3 hover:border-emerald-300 transition-all">
          <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
            <Layers className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 font-outfit">Ensemble ML Pipeline</h3>
          <p className="text-sm text-slate-600">Combines Logistic Regression, Random Forest, XGBoost, and a heterogeneous Stacking Classifier.</p>
        </div>

        <div className="p-6 rounded-2xl bg-white border border-slate-200 custom-shadow space-y-3 hover:border-emerald-300 transition-all">
          <div className="w-12 h-12 rounded-xl bg-teal-100 text-teal-700 flex items-center justify-center">
            <Cpu className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 font-outfit">SHAP Explainability</h3>
          <p className="text-sm text-slate-600">Game-theoretic feature attribution breakdowns for transparent individual explanations.</p>
        </div>

        <div className="p-6 rounded-2xl bg-white border border-slate-200 custom-shadow space-y-3 hover:border-emerald-300 transition-all">
          <div className="w-12 h-12 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center">
            <FileCheck className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 font-outfit">Evidence-Based Data</h3>
          <p className="text-sm text-slate-600">Trained on real public datasets from the UCI ML Repository (Dataset ID: 544).</p>
        </div>

        <div className="p-6 rounded-2xl bg-white border border-slate-200 custom-shadow space-y-3 hover:border-emerald-300 transition-all">
          <div className="w-12 h-12 rounded-xl bg-purple-100 text-purple-700 flex items-center justify-center">
            <Shield className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 font-outfit">Responsible AI</h3>
          <p className="text-sm text-slate-600">Zero PII collection, rigorous leakage-safe preprocessing, and human-in-the-loop oversight.</p>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="bg-white rounded-3xl p-8 border border-slate-200 custom-shadow space-y-8">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 font-outfit">How It Works</h2>
          <p className="text-slate-600 text-sm max-w-xl mx-auto">Seamless decision-support workflow from input to SHAP feature breakdown.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 relative">
          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-3">
            <div className="text-2xl font-black text-emerald-600 font-outfit">01</div>
            <h4 className="font-bold text-slate-900">Enter Information</h4>
            <p className="text-xs text-slate-600">Input physical metrics, dietary habits, and physical activity levels.</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-3">
            <div className="text-2xl font-black text-emerald-600 font-outfit">02</div>
            <h4 className="font-bold text-slate-900">AI Evaluates Risk</h4>
            <p className="text-xs text-slate-600">FastAPI backend runs preprocessed features through the trained ensemble pipeline.</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-3">
            <div className="text-2xl font-black text-emerald-600 font-outfit">03</div>
            <h4 className="font-bold text-slate-900">Understand Why</h4>
            <p className="text-xs text-slate-600">Interactive SHAP charts reveal positive and negative factor contributions.</p>
          </div>

          <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-3">
            <div className="text-2xl font-black text-emerald-600 font-outfit">04</div>
            <h4 className="font-bold text-slate-900">Informed Decisions</h4>
            <p className="text-xs text-slate-600">Helps dietitians and health workers prioritize individuals for formal assessment.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Hero;
