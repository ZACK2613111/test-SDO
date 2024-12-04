'use client'
import { Grid, Box } from '@mui/material';
import PageContainer from '@/app/(DashboardLayout)/components/container/PageContainer';
// components
import TopPayingClients from '@/app/(DashboardLayout)/components/dashboard/TopPayingClients';

const Tasks = () => {
  return (
    <PageContainer title="Tasks" description="This is your tasks">
      <Box>
        <Grid container spacing={3}>
          <Grid item xs={12} lg={8} mx={"auto"}>
            <TopPayingClients />
          </Grid>
        </Grid>
      </Box>
    </PageContainer>
  )
}

export default Tasks;
