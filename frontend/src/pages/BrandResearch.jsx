import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert
} from '@mui/material'
import { api } from '../services/api'

function BrandResearch() {
  const [brands, setBrands] = useState([])
  const [loading, setLoading] = useState(false)
  const [researching, setResearching] = useState(false)
  const [brandName, setBrandName] = useState('')
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  
  useEffect(() => {
    fetchBrands()
  }, [])
  
  const fetchBrands = async () => {
    setLoading(true)
    try {
      const response = await api.getBrands()
      setBrands(response.data.data || [])
    } catch (err) {
      setError('Failed to fetch brands')
    } finally {
      setLoading(false)
    }
  }
  
  const handleResearch = async () => {
    if (!brandName.trim()) {
      setError('Please enter a brand name')
      return
    }
    
    setResearching(true)
    setError(null)
    setSuccess(null)
    
    try {
      const response = await api.researchBrand(brandName)
      setSuccess('Brand researched successfully!')
      setBrandName('')
      fetchBrands()
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to research brand')
    } finally {
      setResearching(false)
    }
  }
  
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Brand Research
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            fullWidth
            label="Brand Name"
            variant="outlined"
            value={brandName}
            onChange={(e) => setBrandName(e.target.value)}
            placeholder="Enter brand name..."
          />
          <Button
            variant="contained"
            onClick={handleResearch}
            disabled={researching}
            sx={{ minWidth: 150 }}
          >
            {researching ? <CircularProgress size={24} /> : 'Research Brand'}
          </Button>
        </Box>
        
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 2 }}>{success}</Alert>}
      </Paper>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Domain</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Social Media</TableCell>
              <TableCell>Created At</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  <CircularProgress />
                </TableCell>
              </TableRow>
            ) : brands.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  No brands found
                </TableCell>
              </TableRow>
            ) : (
              brands.map((brand, index) => (
                <TableRow key={index}>
                  <TableCell>{brand.name || '-'}</TableCell>
                  <TableCell>{brand.domain || '-'}</TableCell>
                  <TableCell>{brand.email || '-'}</TableCell>
                  <TableCell>{typeof brand.social_media === 'object' ? JSON.stringify(brand.social_media) : brand.social_media || '-'}</TableCell>
                  <TableCell>{brand.created_at || '-'}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default BrandResearch

