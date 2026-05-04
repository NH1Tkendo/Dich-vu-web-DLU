/**
 * api.js – Centralised Axios instance for Ebook2LaTeX backend communication.
 *
 * Base URL is read from the Vite environment variable VITE_API_BASE_URL
 * (defined in frontend/.env).  Falls back to http://localhost:8000 for local dev.
 *
 * Usage:
 *   import api from '@/services/api';
 *   const res = await api.post('/upload', formData);
 */
import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

const api = axios.create({
  baseURL: `${BASE_URL}/api/v1`,
  headers: {
    Accept: 'application/json',
  },
  timeout: 30_000, // 30 s – generous for OCR processing
});

// ── Request interceptor ────────────────────────────────────────────
api.interceptors.request.use(
  (config) => {
    // TODO (Phase 3): attach auth token if needed
    // config.headers.Authorization = `Bearer ${getToken()}`;
    return config;
  },
  (error) => Promise.reject(error),
);

// ── Response interceptor ───────────────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status  = error.response?.status;
    const detail  = error.response?.data?.detail;
    const message = detail?.message ?? error.message ?? 'An unexpected error occurred.';

    console.error(`[API] ${status ?? 'Network'} — ${message}`, error);

    // Re-throw a normalised error so components can display it
    return Promise.reject({ status, message, raw: error });
  },
);

export default api;

// ── Typed API helpers (Phase 1 – mock endpoints) ──────────────────
export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const processDocument = (documentId) =>
  api.post(`/process/${documentId}`);

export const listFormulas = (documentId, { page = 1, pageSize = 10 } = {}) =>
  api.get(`/formulas/${documentId}`, { params: { page, page_size: pageSize } });

export const updateFormula = (formulaId, payload) =>
  api.put(`/formulas/${formulaId}`, payload);

export const batchUpdateFormulas = (formulas) =>
  api.post('/formulas/batch', { formulas });
