import React, { useEffect, useState } from 'react'
import { Grid, Typography, Box } from '@mui/material'
import { api } from '../services/api'
import StatCard from '../components/StatCard'

function Dashboard() {
  const [stats, setStats] = useState({
    sellers: 0,
    brands: 0,
    qaCompleted: 0
  })
  
  useEffect(() => {
    fetchStats()
  }, [])
  
  const fetchStats = async () => {
    try {
      const [sellersRes, brandsRes] = await Promise.all([
        api.getSellers(),
        api.getBrands()
      ])
      
      setStats({
        sellers: sellersRes.data.data?.length || 0,
        brands: brandsRes.data.data?.length || 0,
        qaCompleted: 0
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }
  
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={4}>
          <StatCard title="Total Sellers" value={stats.sellers} />
        </Grid>
        <Grid item xs={12} sm={4}>
          <StatCard title="Total Brands" value={stats.brands} />
        </Grid>
        <Grid item xs={12} sm={4}>
          <StatCard title="QA Completed" value={stats.qaCompleted} />
        </Grid>
      </Grid>
    </Box>
  )
}

export default Dashboard

