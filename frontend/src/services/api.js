import axios from 'axios';

const api = axios.create({
  baseURL: 'https://8000-ihia78ehq6oi6tkbljqri-02b9cc79.sandbox.novita.ai/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API方法
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData)
};

export const enterpriseAPI = {
  list: (params) => api.get('/enterprises', { params }),
  get: (id) => api.get(`/enterprises/${id}`),
  create: (data) => api.post('/enterprises', data),
  update: (id, data) => api.put(`/enterprises/${id}`, data),
  verify: (id, approve) => api.post(`/enterprises/${id}/verify`, null, { params: { approve } })
};

export const demandAPI = {
  list: (params) => api.get('/demands', { params }),
  get: (id) => api.get(`/demands/${id}`),
  create: (data) => api.post('/demands', data),
  update: (id, data) => api.put(`/demands/${id}`, data),
  submit: (id) => api.post(`/demands/${id}/submit`),
  evaluate: (id) => api.post(`/demands/${id}/evaluate`),
  match: (id, topK = 5) => api.post(`/demands/${id}/match`, null, { params: { top_k: topK } }),
  delete: (id) => api.delete(`/demands/${id}`)
};

export default api;
