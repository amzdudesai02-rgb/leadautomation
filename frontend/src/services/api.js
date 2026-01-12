import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Store token
let authToken = null

// Set token function
export const setAuthToken = (token) => {
  authToken = token
  if (token) {
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete apiClient.defaults.headers.common['Authorization']
  }
}

// Initialize token from localStorage
const storedToken = localStorage.getItem('token')
if (storedToken) {
  setAuthToken(storedToken)
}

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error)
  }
)

export const api = {
  // Set token
  setToken: (token) => {
    setAuthToken(token)
  },
  
  // Authentication
  login: (username, password) => apiClient.post('/api/auth/login', { username, password }),
  register: (data) => apiClient.post('/api/auth/register', data),
  getCurrentUser: () => apiClient.get('/api/auth/me'),
  logout: () => apiClient.post('/api/auth/logout'),
  
  // Sellers
  getSellers: (params) => apiClient.get('/api/sellers', { params }),
  getSeller: (id) => apiClient.get(`/api/sellers/${id}`),
  scrapeSeller: (url) => apiClient.post('/api/sellers/scrape', { url }),
  updateSeller: (id, data) => apiClient.put(`/api/sellers/${id}`, data),
  deleteSeller: (id) => apiClient.delete(`/api/sellers/${id}`),
  
  // Brands
  getBrands: (params) => apiClient.get('/api/brands', { params }),
  getBrand: (id) => apiClient.get(`/api/brands/${id}`),
  researchBrand: (brandName) => apiClient.post('/api/brands/research', { brand_name: brandName }),
  
  // QA Analysis
  analyzeQA: (brandId) => apiClient.post('/api/qa/analyze', { brand_id: brandId }),
  getQAMetrics: (brandId) => apiClient.get(`/api/qa/metrics/${brandId}`),
}

