import React, { useState, useEffect } from 'react'
import {
  Box,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
  Paper,
  CircularProgress,
  Alert,
  Grid,
  Card,
  CardContent
} from '@mui/material'
import { api } from '../services/api'

function QAAnalysis() {
  const [brands, setBrands] = useState([])
  const [selectedBrand, setSelectedBrand] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState(null)
  
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
  
  const handleAnalyze = async () => {
    if (!selectedBrand) {
      setError('Please select a brand')
      return
    }
    
    setAnalyzing(true)
    setError(null)
    
    try {
      const response = await api.analyzeQA(selectedBrand)
      setAnalysis(response.data.data)
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to analyze brand')
    } finally {
      setAnalyzing(false)
    }
  }
  
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        QA Analysis
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
          <FormControl fullWidth>
            <InputLabel>Select Brand</InputLabel>
            <Select
              value={selectedBrand}
              onChange={(e) => setSelectedBrand(e.target.value)}
              label="Select Brand"
            >
              {brands.map((brand, index) => (
                <MenuItem key={index} value={brand.id || index}>
                  {brand.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <Button
            variant="contained"
            onClick={handleAnalyze}
            disabled={analyzing || !selectedBrand}
            sx={{ minWidth: 150 }}
          >
            {analyzing ? <CircularProgress size={24} /> : 'Analyze'}
          </Button>
        </Box>
        
        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      </Paper>
      
      {analysis && (
        <Grid container spacing={3}>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Profit Margin
                </Typography>
                <Typography variant="h4">
                  {analysis.profit_margin}%
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Competition Score
                </Typography>
                <Typography variant="h4">
                  {analysis.competition_score}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent>
                <Typography color="textSecondary" gutterBottom>
                  Status
                </Typography>
                <Typography variant="h4" color={analysis.status === 'profitable' ? 'success.main' : 'error.main'}>
                  {analysis.status}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  )
}

export default QAAnalysis

