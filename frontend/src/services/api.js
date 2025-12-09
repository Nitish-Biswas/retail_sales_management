import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE;
console.log("API JHKJH URL:", API_BASE);
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const transactionService = {
  getTransactions: async (filters) => {
    const params = new URLSearchParams();
    
    if (filters.search) params.append('search', filters.search);
    if (filters.customer_region?.length) {
      filters.customer_region.forEach(r => params.append('customer_region', r));
    }
    if (filters.gender?.length) {
      filters.gender.forEach(g => params.append('gender', g));
    }
    if (filters.age_min !== undefined && filters.age_min !== null) {
      params.append('age_min', filters.age_min);
    }
    if (filters.age_max !== undefined && filters.age_max !== null) {
      params.append('age_max', filters.age_max);
    }
    if (filters.product_category?.length) {
      filters.product_category.forEach(c => params.append('product_category', c));
    }
    if (filters.tags?.length) {
      filters.tags.forEach(t => params.append('tags', t));
    }
    if (filters.payment_method?.length) {
      filters.payment_method.forEach(p => params.append('payment_method', p));
    }
    if (filters.date_from) params.append('date_from', filters.date_from);
    if (filters.date_to) params.append('date_to', filters.date_to);
    
    params.append('sort_by', filters.sort_by || 'date');
    params.append('sort_order', filters.sort_order || 'desc');
    params.append('page', filters.page);
    params.append('page_size', filters.page_size);
    
    const response = await api.get('/transactions', { params });
    return response.data;
  },
  
  getFilterOptions: async () => {
    const response = await api.get('/filter-options');
    return response.data;
  },
};