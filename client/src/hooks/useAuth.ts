import { useState, useCallback } from "react";
import axios from "axios";
import { useDispatch } from "react-redux";
import { setAuth, clearAuth } from "@/app/redux/slices/authSlice";

export const useAuth = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const dispatch = useDispatch();

  const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: { "Content-Type": "application/json" },
    withCredentials: true,
  });

  const handleRequest = async (callback: () => Promise<any>) => {
    setLoading(true);
    setError(null); // Reset error
    try {
      const response = await callback();
      setLoading(false);
      return response.data;
    } catch (err: any) {
      setLoading(false);
      if (err.response) {
        const message = err.response?.data?.detail || "An error occurred";
        setError(message);
      } else if (err.request) {
        setError("Network error. Please check your internet connection.");
      } else {
        setError("An unexpected error occurred.");
      }
      throw new Error(err.response?.data?.detail || err.message || "Unknown error");
    }
  };

  const register = useCallback(
    (credentials: { name: string; email: string; password: string }) =>
      handleRequest(() =>
        apiClient.post("/auth/register", credentials).then((response) => {
          const { access_token, user_id } = response.data;
          sessionStorage.setItem("authToken", access_token);
          dispatch(setAuth({ token: access_token, userId: user_id }));
          return response;
        })
      ),
    [apiClient, dispatch]
  );

  const login = useCallback(
    (credentials: { email: string; password: string }) =>
      handleRequest(() =>
        apiClient.post("/auth/login", credentials).then((response) => {
          const { access_token, user_id } = response.data;
          sessionStorage.setItem("authToken", access_token);
          dispatch(setAuth({ token: access_token, userId: user_id }));
          return response;
        })
      ),
    [apiClient, dispatch]
  );

  const logout = useCallback(() =>
    handleRequest(async () => {
      await apiClient.post("/auth/logout");
      sessionStorage.removeItem("authToken");
      dispatch(clearAuth());
    }), [apiClient, dispatch]);

  return { register, login, logout, loading, error };
};
