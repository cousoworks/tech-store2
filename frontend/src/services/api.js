import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to add auth token
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

// Add a response interceptor for handling common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized errors
    if (error.response && error.response.status === 401) {
      // Clear local storage and redirect to login if not already there
      if (window.location.pathname !== '/login') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Auth API calls
export const authAPI = {
  login: (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  register: (userData) => api.post('/auth/register', userData),
};

// User API calls
export const userAPI = {
  getCurrentUser: () => api.get('/users/me'),
  updateProfile: (userData) => api.put('/users/me', userData),
};

// Product API calls
export const productAPI = {
  getProducts: (params) => api.get('/products', { params }),
  getProduct: (id) => api.get(`/products/${id}`),
  getPopularProducts: () => api.get('/products/popular'),
  getNewProducts: () => api.get('/products/new'),
  createProduct: (productData) => {
    const formData = new FormData();
    
    // Append text fields
    Object.keys(productData).forEach((key) => {
      if (key !== 'image') {
        formData.append(key, productData[key]);
      }
    });
    
    // Append image if it exists
    if (productData.image) {
      formData.append('image', productData.image);
    }
    
    return api.post('/products', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  updateProduct: (id, productData) => {
    const formData = new FormData();
    
    // Append text fields
    Object.keys(productData).forEach((key) => {
      if (key !== 'image') {
        formData.append(key, productData[key]);
      }
    });
    
    // Append image if it exists
    if (productData.image) {
      formData.append('image', productData.image);
    }
    
    return api.put(`/products/${id}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  deleteProduct: (id) => api.delete(`/products/${id}`),
  getMyProducts: () => api.get('/products/my-products'),
};

// Category API calls
export const categoryAPI = {
  getCategories: () => api.get('/categories'),
  getCategory: (id) => api.get(`/categories/${id}`),
  createCategory: (categoryData) => api.post('/categories', categoryData),
  updateCategory: (id, categoryData) => api.put(`/categories/${id}`, categoryData),
  deleteCategory: (id) => api.delete(`/categories/${id}`),
};

// Review API calls
export const reviewAPI = {
  getProductReviews: (productId) => api.get(`/reviews/product/${productId}`),
  createReview: (reviewData) => api.post('/reviews', reviewData),
  deleteReview: (id) => api.delete(`/reviews/${id}`),
};

// Order API calls
export const orderAPI = {
  getMyOrders: () => api.get('/orders/my-orders'),
  createOrder: (orderItems) => api.post('/orders', { order_items: orderItems }),
  getOrder: (id) => api.get(`/orders/${id}`),
  getAllOrders: () => api.get('/orders'), // Admin only
  updateOrderStatus: (id, status) => api.put(`/orders/${id}/status?status=${status}`), // Admin only
};

export default api;
