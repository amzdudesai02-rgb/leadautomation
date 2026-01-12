// Simple test version - use this to test if React is working
import React from 'react'

function SimpleApp() {
  return (
    <div style={{
      padding: '50px',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      minHeight: '100vh',
      color: 'white',
      textAlign: 'center'
    }}>
      <h1 style={{ fontSize: '48px', marginBottom: '20px' }}>✅ React is Working!</h1>
      <p style={{ fontSize: '24px' }}>If you see this, React is loading correctly.</p>
      <p style={{ marginTop: '20px' }}>The blank page issue is likely in the main App component.</p>
    </div>
  )
}

export default SimpleApp

