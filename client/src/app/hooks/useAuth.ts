    import { useState } from "react";
    import axios from "axios";
    import { useDispatch } from "react-redux";
    import { clearAuth, setAuth } from "../redux/slices/authSlice";

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
        setError(null);
        try {
        const response = await callback();
        setLoading(false);
        return response.data;
        } catch (err: any) {
        setLoading(false);
        const message = err.response?.data?.detail || "An error occurred";
        setError(message);
        throw new Error(message);
        }
    };

    const login = (credentials: { email: string; password: string }) =>
        handleRequest(() =>
        apiClient.post("/auth/login", credentials).then((response) => {
            const { access_token, user_id } = response.data;
            dispatch(setAuth({ token: access_token, userId: user_id }));
            return response;
        })
        );

 
           const register = (credentials: { name: string; email: string; password: string }) =>
                handleRequest(() =>
                  apiClient.post("/auth/register", credentials).then((response) => {
                    const { user_id, email, name } = response.data;
                    dispatch(setAuth({ token: response.data.access_token, userId: user_id }));
                    return response;
                  })
                );
    const logout = () =>
        handleRequest(() => {
        return apiClient.post("/auth/logout").then(() => {
            dispatch(clearAuth());
        });
        });

    const getTasks = (userId: string) =>
        handleRequest(() => apiClient.get(`/tasks/${userId}`));

    return { login, logout, getTasks,register, loading, error };
    };
