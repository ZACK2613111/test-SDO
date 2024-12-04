"use client";
import React, { useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import { Box, Typography } from "@mui/material";

const Logout: React.FC = () => {
  const { logout, loading, error } = useAuth();

  useEffect(() => {
    const handleLogout = async () => {
      try {
        console.log("Attempting to log out...");
        await logout();
        console.log("Logout successful");
        window.location.href = "/authentication/login";
      } catch (err) {
        console.error("Logout error:", err);
      }
    };
    handleLogout();
  }, [logout]);

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      sx={{ width: "100%", minHeight: "100vh" }}
    >
      <Typography variant="h4" mb={2}>
        Logging out...
      </Typography>
      {loading && <Typography variant="body1">Please wait while we log you out...</Typography>}
      {error && <Typography color="error">Error: {error}</Typography>}
    </Box>
  );
};

export default Logout;
