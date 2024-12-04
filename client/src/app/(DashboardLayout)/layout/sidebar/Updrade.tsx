import { Box, Button } from "@mui/material";
import Link from "next/link";

export const Upgrade = () => {
  return (
    <Box
      display={"flex"}
      alignItems="center"
      gap={2}
      sx={{ m: 3}}
    >
      <>
        <Button
          color="primary"
          target="_blank"
          disableElevation
          component={Link}
          href=""
          variant="contained"
          aria-label="logout"
          size="large" sx={{width: "100%"}}
        >
          Upgrade
        </Button>
      </>
    </Box>
  );
};
