import React, { useState } from "react";
import {
  Box,
  Typography,
  FormGroup,
  FormControlLabel,
  Button,
  Stack,
  Checkbox,
  Alert,
} from "@mui/material";
import Link from "next/link";
import CustomTextField from "@/app/(DashboardLayout)/components/forms/theme-elements/CustomTextField";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";

interface LoginProps {
  title?: string;
  subtitle?: JSX.Element | JSX.Element[];
  subtext?: JSX.Element | JSX.Element[];
}

const AuthLogin: React.FC<LoginProps> = ({ title, subtitle, subtext }) => {
  const { login, loading, error } = useAuth();
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [rememberMe, setRememberMe] = useState<boolean>(true);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await login({ email, password });
      router.push("/"); // Use next.js router for internal navigation
    } catch (err) {
      console.error("Login failed", err);
    }
  };

  return (
    <>
      {title && (
        <Typography variant="h2" fontWeight="700" mb={1}>
          {title}
        </Typography>
      )}
      {subtext}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      <form onSubmit={handleLogin}>
        <Stack spacing={2}>
          <Box>
            <Typography variant="subtitle1" fontWeight={600} component="label" htmlFor="email" mb={1}>
              Email
            </Typography>
            <CustomTextField
              id="email"
              type="email"
              value={email}
              onChange={(e : React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
              fullWidth
              required
            />
          </Box>
          <Box mt={3}>
            <Typography variant="subtitle1" fontWeight={600} component="label" htmlFor="password" mb={1}>
              Password
            </Typography>
            <CustomTextField
              id="password"
              type="password"
              value={password}
              onChange={(e : React.ChangeEvent<HTMLInputElement>) => setPassword(e.target.value)}
              fullWidth
              required
            />
          </Box>
          <Stack direction="row" justifyContent="space-between" alignItems="center" my={2}>
            <FormGroup>
              <FormControlLabel
                control={<Checkbox checked={rememberMe} onChange={(e) => setRememberMe(e.target.checked)} />}
                label="Remember this Device"
              />
            </FormGroup>
            <Typography component={Link} href="/forgot-password" fontWeight="500" sx={{ color: "primary.main" }}>
              Forgot Password?
            </Typography>
          </Stack>
        </Stack>
        <Box>
          <Button color="primary" variant="contained" size="large" fullWidth type="submit" disabled={loading}>
            {loading ? "Signing In..." : "Sign In"}
          </Button>
        </Box>
      </form>
      {subtitle}
    </>
  );
};

export default AuthLogin;
