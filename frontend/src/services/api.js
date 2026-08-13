import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 90000, // 90s timeout to allow Render/free tier backends to wake up from cold starts
});

export const getHealth = async (retries = 3, delayMs = 3000) => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await apiClient.get('/health', { timeout: 90000 });
      return response.data;
    } catch (error) {
      console.warn(`Health check attempt ${attempt}/${retries} failed:`, error.message);
      if (attempt === retries) {
        return { status: 'offline', model_loaded: false, error: error.message };
      }
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }
};

export const predictNutritionalRisk = async (profileData) => {
  try {
    const response = await apiClient.post('/api/predict', profileData, {
      timeout: 120000, // 120s for predictions during initial startup
    });
    return response.data;
  } catch (error) {
    console.error('Prediction API error:', error);
    throw error;
  }
};

export const getModelInfo = async (retries = 2, delayMs = 3000) => {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await apiClient.get('/api/model-info', { timeout: 90000 });
      return response.data;
    } catch (error) {
      console.warn(`Model info API attempt ${attempt}/${retries} failed:`, error.message);
      if (attempt === retries) throw error;
      await new Promise((resolve) => setTimeout(resolve, delayMs));
    }
  }
};

export default apiClient;

