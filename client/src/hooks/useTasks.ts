import { useState } from "react";
import axios from "axios";

export const useTasks = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [tasks, setTasks] = useState<any[]>([]);

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

  const getTasks = (userId: string) =>
    handleRequest(() =>
      apiClient.get(`/tasks/${userId}`).then((response) => {
        setTasks(response.data);
        return response;
      })
    );

    const createTask = (task: { title: string; description: string; is_completed: boolean }) =>
    handleRequest(() =>
      apiClient.post(`/tasks/`, task).then((response) => {
        setTasks((prevTasks) => [...prevTasks, response.data]);
        return response;
      })
    );

  const updateTask = (taskId: number, task: { title: string; description: string; is_completed: boolean }) =>
    handleRequest(() =>
      apiClient.put(`/tasks/${taskId}`, task).then((response) => {
        setTasks((prevTasks) =>
          prevTasks.map((t) => (t.id === taskId ? response.data : t))
        );
        return response;
      })
    );
  const deleteTask = (taskId: number) =>
    handleRequest(() =>
      apiClient.delete(`/tasks/${taskId}`).then(() => {
        setTasks((prevTasks) => prevTasks.filter((t) => t.id !== taskId));
      })
    );

  return {
    tasks,
    getTasks,
    createTask,
    updateTask,
    deleteTask,
    loading,
    error,
  };
};
