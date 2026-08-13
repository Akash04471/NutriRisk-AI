import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import InputSection from './components/InputSection';
import RiskCard from './components/RiskCard';
import ShapExplanation from './components/ShapExplanation';
import ModelComparison from './components/ModelComparison';
import ResponsibleAI from './components/ResponsibleAI';
import Footer from './components/Footer';
import { getHealth, predictNutritionalRisk, getModelInfo } from './services/api';
import { AlertCircle, RefreshCw } from 'lucide-react';

const App = () => {
  const [activeTab, setActiveTab] = useState('home');
  const [apiStatus, setApiStatus] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);

  // 16 Verified Dataset Input Features Initial State
  const [formData, setFormData] = useState({
    Gender: 'Female',
    Age: 24.0,
    Height: 1.65,
    Weight: 72.0,
    family_history_with_overweight: 'yes',
    FAVC: 'yes',
    FCVC: 2.0,
    NCP: 3.0,
    CAEC: 'Sometimes',
    SMOKE: 'no',
    CH2O: 2.0,
    SCC: 'no',
    FAF: 1.0,
    TUE: 1.0,
    CALC: 'Sometimes',
    MTRANS: 'Public_Transportation',
  });

  const [predictionResult, setPredictionResult] = useState(null);

  // Check FastAPI Health & Model Info on mount
  useEffect(() => {
    const checkBackend = async () => {
      const health = await getHealth();
      setApiStatus(health);

      try {
        const info = await getModelInfo();
        setModelInfo(info);
      } catch (err) {
        console.warn('Failed to load model metrics:', err.message);
      }
    };
    checkBackend();
  }, []);

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage(null);

    try {
      const result = await predictNutritionalRisk(formData);
      setPredictionResult(result);
      // Smooth scroll to results
      setTimeout(() => {
        const resultsEl = document.getElementById('results-dashboard');
        if (resultsEl) {
          resultsEl.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } catch (err) {
      console.error('Prediction submission error:', err);
      if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
        setErrorMessage(
          'Backend server response timed out. Free-tier backend instances (e.g. Render) spin down when inactive and take 30-60 seconds to wake up. Please wait a moment and click "Analyze Nutritional Risk" again.'
        );
      } else {
        setErrorMessage(
          err.response?.data?.detail || 'Unable to connect to NutriRisk AI FastAPI backend. Please verify that the backend server is running and VITE_API_BASE_URL environment variable is set in Vercel.'
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} apiStatus={apiStatus} />

      <main className="flex-grow max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-12 w-full">
        
        {/* Error Alert Banner */}
        {errorMessage && (
          <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start space-x-3 shadow-md">
            <AlertCircle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
            <div>
              <strong className="font-bold">Backend Connection Error:</strong> {errorMessage}
            </div>
          </div>
        )}

        {/* Tab 1: Overview / Home */}
        {activeTab === 'home' && (
          <Hero onStart={() => setActiveTab('assessment')} />
        )}

        {/* Tab 2: Risk Assessment Form & Results */}
        {activeTab === 'assessment' && (
          <div className="space-y-12">
            <InputSection
              formData={formData}
              setFormData={setFormData}
              onSubmit={handleFormSubmit}
              isLoading={isLoading}
            />

            {/* Results Dashboard */}
            {predictionResult && (
              <div id="results-dashboard" className="space-y-8 pt-4 border-t border-slate-200">
                <div className="text-center space-y-1">
                  <span className="px-3 py-1 bg-emerald-100 text-emerald-800 font-extrabold text-xs rounded-full uppercase tracking-wider">
                    Prediction Generated
                  </span>
                  <h2 className="text-3xl font-extrabold text-slate-900 font-outfit">Screening Analysis Results</h2>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <RiskCard result={predictionResult} />
                  <ShapExplanation explanation={predictionResult.explanation} />
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 3: Model Metrics & Architecture */}
        {activeTab === 'metrics' && (
          <ModelComparison modelInfo={modelInfo} />
        )}

        {/* Tab 4: Responsible AI */}
        {activeTab === 'ethics' && (
          <ResponsibleAI />
        )}

      </main>

      <Footer />
    </div>
  );
};

export default App;
