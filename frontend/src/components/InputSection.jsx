import React from 'react';
import { User, Activity, Utensils, RefreshCw, Zap } from 'lucide-react';

const InputSection = ({ formData, setFormData, onSubmit, isLoading }) => {
  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const loadPresetHighRisk = () => {
    setFormData({
      Gender: 'Male',
      Age: 26.0,
      Height: 1.70,
      Weight: 92.0,
      family_history_with_overweight: 'yes',
      FAVC: 'yes',
      FCVC: 1.0,
      NCP: 3.0,
      CAEC: 'Frequently',
      SMOKE: 'no',
      CH2O: 1.0,
      SCC: 'no',
      FAF: 0.0,
      TUE: 2.0,
      CALC: 'Sometimes',
      MTRANS: 'Public_Transportation'
    });
  };

  const loadPresetLowRisk = () => {
    setFormData({
      Gender: 'Female',
      Age: 22.0,
      Height: 1.68,
      Weight: 58.0,
      family_history_with_overweight: 'no',
      FAVC: 'no',
      FCVC: 3.0,
      NCP: 3.0,
      CAEC: 'Sometimes',
      SMOKE: 'no',
      CH2O: 3.0,
      SCC: 'yes',
      FAF: 2.0,
      TUE: 0.5,
      CALC: 'no',
      MTRANS: 'Walking'
    });
  };

  return (
    <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 custom-shadow space-y-8">
      {/* Header & Presets */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-900 font-outfit">Nutritional Risk Assessment</h2>
          <p className="text-sm text-slate-600">Enter the required patient profile information to generate an explainable risk score.</p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={loadPresetHighRisk}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-50 text-rose-700 hover:bg-rose-100 border border-rose-200 transition-all flex items-center space-x-1"
          >
            <Zap className="w-3.5 h-3.5" />
            <span>Preset: High Risk</span>
          </button>
          <button
            type="button"
            onClick={loadPresetLowRisk}
            className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border border-emerald-200 transition-all flex items-center space-x-1"
          >
            <Zap className="w-3.5 h-3.5" />
            <span>Preset: Low Risk</span>
          </button>
        </div>
      </div>

      <form onSubmit={onSubmit} className="space-y-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Card 1: Personal & Physical */}
          <div className="space-y-5 p-5 rounded-2xl bg-slate-50/70 border border-slate-200/80">
            <div className="flex items-center space-x-2 font-bold text-slate-900 text-base font-outfit border-b border-slate-200 pb-3">
              <User className="w-5 h-5 text-emerald-600" />
              <span>Demographics & Body Metrics</span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Gender</label>
              <select
                value={formData.Gender}
                onChange={(e) => handleChange('Gender', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="Female">Female</option>
                <option value="Male">Male</option>
              </select>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Age (years)</span>
                <span className="text-emerald-700 font-bold">{formData.Age} yrs</span>
              </div>
              <input
                type="range"
                min="14"
                max="80"
                step="1"
                value={formData.Age}
                onChange={(e) => handleChange('Age', parseFloat(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Height (meters)</span>
                <span className="text-emerald-700 font-bold">{formData.Height} m</span>
              </div>
              <input
                type="range"
                min="1.40"
                max="2.10"
                step="0.01"
                value={formData.Height}
                onChange={(e) => handleChange('Height', parseFloat(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Weight (kg)</span>
                <span className="text-emerald-700 font-bold">{formData.Weight} kg</span>
              </div>
              <input
                type="range"
                min="35"
                max="160"
                step="0.5"
                value={formData.Weight}
                onChange={(e) => handleChange('Weight', parseFloat(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Family History of Overweight</label>
              <select
                value={formData.family_history_with_overweight}
                onChange={(e) => handleChange('family_history_with_overweight', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="yes">Yes</option>
                <option value="no">No</option>
              </select>
            </div>
          </div>

          {/* Card 2: Dietary Intake Habits */}
          <div className="space-y-5 p-5 rounded-2xl bg-slate-50/70 border border-slate-200/80">
            <div className="flex items-center space-x-2 font-bold text-slate-900 text-base font-outfit border-b border-slate-200 pb-3">
              <Utensils className="w-5 h-5 text-teal-600" />
              <span>Dietary Intake Habits</span>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Frequent High-Calorie Food Intake (FAVC)</label>
              <select
                value={formData.FAVC}
                onChange={(e) => handleChange('FAVC', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="yes">Yes</option>
                <option value="no">No</option>
              </select>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Vegetable Intake Frequency (FCVC)</span>
                <span className="text-teal-700 font-bold">
                  {formData.FCVC <= 1.5 ? '1: Rarely' : formData.FCVC <= 2.5 ? '2: Sometimes' : '3: Always'}
                </span>
              </div>
              <input
                type="range"
                min="1.0"
                max="3.0"
                step="0.5"
                value={formData.FCVC}
                onChange={(e) => handleChange('FCVC', parseFloat(e.target.value))}
                className="w-full accent-teal-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Number of Main Meals (NCP)</span>
                <span className="text-teal-700 font-bold">{formData.NCP} meals</span>
              </div>
              <input
                type="range"
                min="1.0"
                max="4.0"
                step="1.0"
                value={formData.NCP}
                onChange={(e) => handleChange('NCP', parseFloat(e.target.value))}
                className="w-full accent-teal-600 cursor-pointer"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Food Consumption Between Meals (CAEC)</label>
              <select
                value={formData.CAEC}
                onChange={(e) => handleChange('CAEC', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="no">No</option>
                <option value="Sometimes">Sometimes</option>
                <option value="Frequently">Frequently</option>
                <option value="Always">Always</option>
              </select>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Daily Water Intake (CH2O Liters)</span>
                <span className="text-teal-700 font-bold">
                  {formData.CH2O <= 1.5 ? '1: < 1L' : formData.CH2O <= 2.5 ? '2: 1 - 2L' : '3: > 2L'}
                </span>
              </div>
              <input
                type="range"
                min="1.0"
                max="3.0"
                step="0.5"
                value={formData.CH2O}
                onChange={(e) => handleChange('CH2O', parseFloat(e.target.value))}
                className="w-full accent-teal-600 cursor-pointer"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Monitors Daily Caloric Intake (SCC)</label>
              <select
                value={formData.SCC}
                onChange={(e) => handleChange('SCC', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="yes">Yes</option>
                <option value="no">No</option>
              </select>
            </div>
          </div>

          {/* Card 3: Lifestyle & Physical Activity */}
          <div className="space-y-5 p-5 rounded-2xl bg-slate-50/70 border border-slate-200/80">
            <div className="flex items-center space-x-2 font-bold text-slate-900 text-base font-outfit border-b border-slate-200 pb-3">
              <Activity className="w-5 h-5 text-sky-600" />
              <span>Lifestyle & Activity</span>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Physical Activity Frequency (FAF)</span>
                <span className="text-sky-700 font-bold">
                  {formData.FAF === 0 ? '0: None' : formData.FAF <= 1 ? '1: 1-2 days' : formData.FAF <= 2 ? '2: 3-4 days' : '3: 5+ days'}
                </span>
              </div>
              <input
                type="range"
                min="0.0"
                max="3.0"
                step="0.5"
                value={formData.FAF}
                onChange={(e) => handleChange('FAF', parseFloat(e.target.value))}
                className="w-full accent-sky-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Technology Screen Time Hours (TUE)</span>
                <span className="text-sky-700 font-bold">
                  {formData.TUE <= 0.5 ? '0: 0-2 hours' : formData.TUE <= 1.5 ? '1: 3-5 hours' : '2: > 5 hours'}
                </span>
              </div>
              <input
                type="range"
                min="0.0"
                max="2.0"
                step="0.5"
                value={formData.TUE}
                onChange={(e) => handleChange('TUE', parseFloat(e.target.value))}
                className="w-full accent-sky-600 cursor-pointer"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Smoking Habit</label>
              <select
                value={formData.SMOKE}
                onChange={(e) => handleChange('SMOKE', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="no">No</option>
                <option value="yes">Yes</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Alcohol Consumption Frequency</label>
              <select
                value={formData.CALC}
                onChange={(e) => handleChange('CALC', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="no">No</option>
                <option value="Sometimes">Sometimes</option>
                <option value="Frequently">Frequently</option>
                <option value="Always">Always</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Primary Transportation Method</label>
              <select
                value={formData.MTRANS}
                onChange={(e) => handleChange('MTRANS', e.target.value)}
                className="w-full rounded-xl border-slate-300 text-sm focus:ring-emerald-500 focus:border-emerald-500 bg-white p-2.5 border"
              >
                <option value="Public_Transportation">Public Transportation</option>
                <option value="Automobile">Automobile</option>
                <option value="Walking">Walking</option>
                <option value="Motorbike">Motorbike</option>
                <option value="Bike">Bike</option>
              </select>
            </div>
          </div>

        </div>

        {/* Submit CTA Button */}
        <div className="pt-4 border-t border-slate-100 flex flex-col items-center space-y-3">
          <button
            type="submit"
            disabled={isLoading}
            className="w-full sm:w-auto min-w-[320px] bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-extrabold text-lg px-8 py-4 rounded-2xl shadow-xl shadow-emerald-600/30 transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-3"
          >
            {isLoading ? (
              <>
                <RefreshCw className="w-5 h-5 animate-spin" />
                <span>Evaluating Ensemble Pipeline...</span>
              </>
            ) : (
              <>
                <span>Analyze Nutritional Risk</span>
                <Zap className="w-5 h-5" />
              </>
            )}
          </button>

          {isLoading && (
            <p className="text-xs text-slate-500 animate-pulse">
              Running model preprocessing, ensemble inference & calculating SHAP values...
            </p>
          )}
        </div>
      </form>
    </div>
  );
};

export default InputSection;
