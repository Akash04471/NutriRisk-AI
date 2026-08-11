# 🥗 NutriRisk AI — React Frontend Application

Modern React + Vite + Tailwind CSS single page web application for **NutriRisk AI** explainable nutritional risk prediction.

## Tech Stack
* **Framework:** React 18 + Vite 5
* **Styling:** Tailwind CSS 3 + PostCSS + Google Fonts (Inter & Outfit)
* **Charts:** Recharts 2 (Horizontal SHAP contribution bar charts & model metric comparators)
* **Icons:** Lucide React
* **HTTP Client:** Axios 1.7 connecting to FastAPI REST endpoints

## Local Development Execution
```bash
# 1. Install dependencies
npm install

# 2. Start Vite dev server (port 5173)
npm run dev
```

The application will be accessible at [http://localhost:5173](http://localhost:5173).
Ensure the FastAPI backend server (`uvicorn main:app --reload --port 8000`) is running.
