import axios from 'axios'

// Get API URL from environment variable
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

// Log API URL in development (helps debug)
if (import.meta.env.DEV) {
  console.log('🔗 API Base URL:', API_BASE_URL)
}

// Warn if using localhost in production
if (!import.meta.env.DEV && API_BASE_URL.includes('localhost')) {
  console.warn('⚠️ WARNING: Using localhost API URL in production!')
  console.warn('⚠️ Set VITE_API_URL environment variable in Vercel!')
}

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
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
    // Log connection errors for debugging
    if (error.code === 'ERR_NETWORK' || error.code === 'ECONNREFUSED') {
      console.error('❌ Connection Error:', error.message)
      console.error('🔗 Attempted URL:', error.config?.url)
      console.error('📍 Base URL:', API_BASE_URL)
      if (API_BASE_URL.includes('localhost')) {
        console.error('⚠️ Make sure VITE_API_URL is set in Vercel environment variables!')
      }
    }
    
    if (error.response?.status === 401) {
      // Handle unauthorized - clear token and redirect to login
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
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

