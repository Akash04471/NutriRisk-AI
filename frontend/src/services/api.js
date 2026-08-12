import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const getHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'offline', model_loaded: false };
  }
};

export const predictNutritionalRisk = async (profileData) => {
  try {
    const response = await apiClient.post('/api/predict', profileData);
    return response.data;
  } catch (error) {
    console.error('Prediction API error:', error);
    throw error;
  }
};

export const getModelInfo = async () => {
  try {
    const response = await apiClient.get('/api/model-info');
    return response.data;
  } catch (error) {
    console.error('Model info API error:', error);
    throw error;
  }
};

export default apiClient;
