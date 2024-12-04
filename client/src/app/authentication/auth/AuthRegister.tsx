import React, { useState } from "react";
import { Box, Typography, Button, Stack } from "@mui/material";
import CustomTextField from "@/app/(DashboardLayout)/components/forms/theme-elements/CustomTextField";
import { useAuth } from "@/hooks/useAuth";
import Link from "next/link";

const AuthRegister = () => {
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [emailError, setEmailError] = useState<string | null>(null);
  const [nameError, setNameError] = useState<string | null>(null);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const { register, loading, error } = useAuth();

  const validateForm = () => {
    let valid = true;
    setEmailError(null);
    setNameError(null);
    setPasswordError(null);

    if (!name.trim()) {
      setNameError("Name is required");
      valid = false;
    }

    if (name.length > 20) {
      setNameError("Name cannot be longer than 20 characters");
      valid = false;
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email.trim()) {
      setEmailError("Email is required");
      valid = false;
    } else if (!emailPattern.test(email)) {
      setEmailError("Please enter a valid email");
      valid = false;
    }

    if (!password.trim()) {
      setPasswordError("Password is required");
      valid = false;
    } else if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      setPasswordError("Password must contain at least one special character");
      valid = false;
    }

    return valid;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    try {
      await register({ email, password, name });
      window.location.href = "/";
    } catch (err: any) {
      if (err.response?.data?.detail) {
        const errorDetail = err.response.data.detail;
        errorDetail.forEach((error: any) => {
          if (error.loc[1] === "email") setEmailError(error.msg);
          if (error.loc[1] === "name") setNameError(error.msg);
          if (error.loc[1] === "password") setPasswordError(error.msg);
        });
      }
    }
  };

  return (
    <Box>
      <Typography fontWeight="700" variant="h2" mb={1} sx={{ mt: 4 }}>
        Create an Account
      </Typography>
      <Stack spacing={3}>
        <CustomTextField
          label="Name"
          value={name}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setName(e.target.value)}
          variant="outlined"
          fullWidth
          error={!!nameError}
          helperText={nameError}
        />
        <CustomTextField
          label="Email Address"
          type="email"
          value={email}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
          variant="outlined"
          fullWidth
          error={!!emailError}
          helperText={emailError}
        />
        <CustomTextField
          label="Password"
          type="password"
          value={password}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
          variant="outlined"
          fullWidth
          error={!!passwordError}
          helperText={passwordError}
        />
      </Stack>

      {error && (
        <Typography color="error" variant="body2" sx={{ mt: 2 }}>
          {typeof error === "string" ? error : "An error occurred. Please try again."}
        </Typography>
      )}

      <Button
        color="primary"
        variant="contained"
        size="large"
        fullWidth
        onClick={handleSubmit}
        disabled={loading}
        sx={{ mt: 4 }}
      >
        {loading ? "Registering..." : "Sign Up"}
      </Button>

      <Stack justifyContent="center" direction="row" alignItems="center" my={3}>
        <Typography variant="body2" color="textSecondary">
          Already have an account?{" "}
        </Typography>
        <Typography
          component={Link}
          href="/authentication/login"
          fontWeight="500"
          sx={{
            textDecoration: "none",
            color: "primary.main",
            ml: 1,
            "&:hover": {
              textDecoration: "underline",
            },
          }}
        >
          Sign In
        </Typography>
      </Stack>
    </Box>
  );
};

export default AuthRegister;
