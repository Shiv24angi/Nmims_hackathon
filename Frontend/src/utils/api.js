import axios from 'axios';

const api = axios.create({
  baseURL: 'https://smartrasoi-backend-shcx.onrender.com/api',
});

export default api;
