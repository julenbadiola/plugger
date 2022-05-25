import axios from 'axios';
import { getConfig } from '../config';
import useStore from '../state';

const config = getConfig()

const instance = axios.create({
  baseURL: config.apiOrigin,
  timeout: 20000,
});

// Add a request interceptor
instance.interceptors.request.use(function (config) {
  const token = useStore.getState().accessToken
  config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export class GeneralApi {
  async getPlugins() {
    const res = await instance.get(`http://localhost:5005/status`)
    console.log('getPlugins call', res.data);
    return res.data
  }
}


export default new GeneralApi()