import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Button, Box } from '@mui/material'
import { Dashboard, Store, Business, Assessment } from '@mui/icons-material'

function Navigation() {
  const location = useLocation()
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: Dashboard },
    { path: '/sellers', label: 'Sellers', icon: Store },
    { path: '/brands', label: 'Brands', icon: Business },
    { path: '/qa', label: 'QA Analysis', icon: Assessment },
  ]
  
  return (
    <Box sx={{ display: 'flex', gap: 1 }}>
      {navItems.map((item) => {
        const Icon = item.icon
        const isActive = location.pathname === item.path
        return (
          <Button
            key={item.path}
            component={Link}
            to={item.path}
            startIcon={<Icon />}
            sx={{
              color: isActive ? 'white' : 'rgba(255,255,255,0.8)',
              fontWeight: isActive ? 'bold' : 'normal',
              backgroundColor: isActive ? 'rgba(255,255,255,0.2)' : 'transparent',
              '&:hover': {
                backgroundColor: 'rgba(255,255,255,0.15)',
              },
              borderRadius: 2,
              px: 2,
            }}
          >
            {item.label}
          </Button>
        )
      })}
    </Box>
  )
}

export default Navigation

