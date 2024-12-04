"use client"
import { useEffect } from "react";
import { Box, Typography, Button } from "@mui/material";
import { useRouter } from "next/router";

const ErrorPage = ({ statusCode }: { statusCode: number }) => {
  const router = useRouter();

  useEffect(() => {
    if (statusCode === 404) {
      setTimeout(() => {
        router.push("/"); 
      }, 3000);
    }
  }, [statusCode, router]);

  return (
    <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" sx={{ minHeight: "100vh" }}>
      <Typography variant="h2" color="error" mb={2}>
        {statusCode === 404 ? "Page Not Found" : "Something Went Wrong"}
      </Typography>
      <Typography variant="body1" mb={3}>
        {statusCode === 404 ? "We couldn't find the page you're looking for." : "An unexpected error occurred."}
      </Typography>
      <Button variant="contained" color="primary" onClick={() => router.push("/authentication/login")}>
        Go to Homepage
      </Button>
    </Box>
  );
};

ErrorPage.getInitialProps = ({ res, err }: { res: any; err: any }) => {
  const statusCode = res ? res.statusCode : err ? err.statusCode : 404;
  return { statusCode };
};

export default ErrorPage;
