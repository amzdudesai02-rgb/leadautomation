import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'

function StatCard({ title, value }) {
  return (
    <Card>
      <CardContent>
        <Typography color="textSecondary" gutterBottom>
          {title}
        </Typography>
        <Typography variant="h4">
          {value}
        </Typography>
      </CardContent>
    </Card>
  )
}

export default StatCard

