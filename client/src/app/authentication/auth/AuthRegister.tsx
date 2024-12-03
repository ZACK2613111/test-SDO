import React, { useState } from "react";
import { Box, Typography, Button, Stack } from "@mui/material";
import CustomTextField from "@/app/(DashboardLayout)/components/forms/theme-elements/CustomTextField";
import { useAuth } from "@/app/hooks/useAuth";

const AuthRegister = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const { register, loading, error } = useAuth();

  const handleSubmit = async () => {
    try {
      await register({ email, password, name });
      alert("User registered successfully!");
    } catch (err) {
      console.error("Registration error:", err.message);
    }
  };

  return (
    <Box>
      <Typography fontWeight="700" variant="h2" mb={1}>
        Create an Account
      </Typography>
      <Stack spacing={3}>
        <CustomTextField
          label="Name"
          value={name}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
          variant="outlined"
          fullWidth
        />
        <CustomTextField
          label="Email Address"
          type="email"
          value={email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          variant="outlined"
          fullWidth
        />
        <CustomTextField
          label="Password"
          type="password"
          value={password}
          onChange={(e: React.ChangeEvent<HTMLInputElement> ) => setPassword(e.target.value)}
          variant="outlined"
          fullWidth
        />
      </Stack>
      {error && <Typography color="error">{error}</Typography>}
      <Button
        color="primary"
        variant="contained"
        size="large"
        fullWidth
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Registering..." : "Sign Up"}
      </Button>
    </Box>
  );
};

export default AuthRegister;
