'use client';

import React, { useEffect, useState } from "react";
import {
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Chip,
  Checkbox,
  IconButton,
} from "@mui/material";
import { IconEdit, IconTrash } from "@tabler/icons-react";
import DashboardCard from "../shared/DashboardCard";
import { useSelector } from "react-redux";
import { useTasks } from "@/hooks/useTasks";

const TopPayingClients = () => {
  const { getTasks, updateTask, deleteTask, loading, error } = useTasks();
  const userId = useSelector((state: any) => state.auth.userId); // Access userId from Redux
  const [tasks, setTasks] = useState<any[]>([]);

  useEffect(() => {
    const fetchTasks = async () => {
      if (userId) {
        try {
          const fetchedTasks = await getTasks(userId);
          setTasks(fetchedTasks);
        } catch (err) {
          console.error(err);
        }
      }
    };
    fetchTasks();
  }, [userId]);

  const handleUpdateTask = async (taskId: number, updatedTask: any) => {
    try {
      const newTask = await updateTask(taskId, updatedTask);
      setTasks((prev) =>
        prev.map((task) => (task.id === taskId ? newTask : task))
      );
    } catch (err) {
      console.error(err);
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    try {
      await deleteTask(taskId);
      setTasks((prev) => prev.filter((task) => task.id !== taskId));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <DashboardCard title="Tasks">
      <Box>
        {loading && <Typography>Loading tasks...</Typography>}
        {error && <Typography color="error">{error}</Typography>}
        {!loading && !error && (
          <Box sx={{ overflow: "auto" }}>
            <Box sx={{ width: "100%", display: "table", tableLayout: "fixed" }}>
              <Table sx={{ whiteSpace: "nowrap" }}>
                <TableHead>
                  <TableRow>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        Id
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        Description
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        Name
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="subtitle2" fontWeight={600}>
                        Priority
                      </Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Typography variant="subtitle2" fontWeight={600}>
                        Completed
                      </Typography>
                    </TableCell>
                    <TableCell align="center">
                      <Typography variant="subtitle2" fontWeight={600}>
                        Actions
                      </Typography>
                    </TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {tasks.map((task) => (
                    <TableRow key={task.id}>
                      <TableCell>
                        <Typography sx={{ fontSize: "15px", fontWeight: "500" }}>
                          {task.id}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="subtitle2" fontWeight={600}>
                          {task.description}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography
                          color="textSecondary"
                          variant="subtitle2"
                          fontWeight={400}
                        >
                          {task.name}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          sx={{
                            px: "4px",
                            backgroundColor:
                              task.priority === "High"
                                ? "error.main"
                                : task.priority === "Medium"
                                ? "warning.main"
                                : "primary.main",
                            color: "#fff",
                          }}
                          size="small"
                          label={task.priority}
                        />
                      </TableCell>
                      <TableCell align="center">
                        <Checkbox
                          checked={task.is_completed}
                          onChange={(e) =>
                            handleUpdateTask(task.id, {
                              ...task,
                              is_completed: e.target.checked,
                            })
                          }
                        />
                      </TableCell>
                      <TableCell align="center">
                        <IconButton
                          color="primary"
                          onClick={() => console.log("Edit Task", task)}
                        >
                          <IconEdit />
                        </IconButton>
                        <IconButton
                          color="error"
                          onClick={() => handleDeleteTask(task.id)}
                        >
                          <IconTrash />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Box>
        )}
      </Box>
    </DashboardCard>
  );
};

export default TopPayingClients;
