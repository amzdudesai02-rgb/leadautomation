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

function SellerSniping() {
  const [sellers, setSellers] = useState([])
  const [loading, setLoading] = useState(false)
  const [scraping, setScraping] = useState(false)
  const [url, setUrl] = useState('')
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)
  
  useEffect(() => {
    fetchSellers()
  }, [])
  
  const fetchSellers = async () => {
    setLoading(true)
    try {
      const response = await api.getSellers()
      setSellers(response.data.data || [])
    } catch (err) {
      setError('Failed to fetch sellers')
    } finally {
      setLoading(false)
    }
  }
  
  const handleScrape = async () => {
    if (!url.trim()) {
      setError('Please enter a valid URL')
      return
    }
    
    setScraping(true)
    setError(null)
    setSuccess(null)
    
    try {
      const response = await api.scrapeSeller(url)
      setSuccess('Seller scraped successfully!')
      setUrl('')
      fetchSellers()
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to scrape seller')
    } finally {
      setScraping(false)
    }
  }
  
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Seller Sniping
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <TextField
            fullWidth
            label="Amazon Seller URL"
            variant="outlined"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://www.amazon.com/seller/..."
          />
          <Button
            variant="contained"
            onClick={handleScrape}
            disabled={scraping}
            sx={{ minWidth: 150 }}
          >
            {scraping ? <CircularProgress size={24} /> : 'Scrape Seller'}
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
              <TableCell>Email</TableCell>
              <TableCell>Store URL</TableCell>
              <TableCell>Phone</TableCell>
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
            ) : sellers.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} align="center">
                  No sellers found
                </TableCell>
              </TableRow>
            ) : (
              sellers.map((seller, index) => (
                <TableRow key={index}>
                  <TableCell>{seller.name || '-'}</TableCell>
                  <TableCell>{seller.email || '-'}</TableCell>
                  <TableCell>{seller.store_url || '-'}</TableCell>
                  <TableCell>{seller.phone || '-'}</TableCell>
                  <TableCell>{seller.created_at || '-'}</TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  )
}

export default SellerSniping

