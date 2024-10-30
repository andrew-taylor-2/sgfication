import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { CssBaseline, GlobalStyles, Box, Toolbar } from '@mui/material';
import NavDrawer from './components/NavDrawer';
import About from './components/About';
import Bio from './components/Bio';
import Board from './components/Board';

const globalStyles = (
  <GlobalStyles
    styles={{
      'html, body': {
        backgroundColor: '#646464',
        margin: 0,
        padding: 0,
        minHeight: '100vh',
        fontFamily: 'Roboto, sans-serif',
      },
      '#root': {
        minHeight: '100vh',
        backgroundColor: '#646464',
      }
    }}
  />
);

function App() {
  const [sgfData, setSgfData] = useState(null);
  
  return (
    <>
      <CssBaseline />
      {globalStyles}
      <Router>
        <Box sx={{ 
          display: 'flex',
          minHeight: '100vh',
          backgroundColor: '#646464'
        }}>
          <NavDrawer />
          <Box
            component="main"
            sx={{
              flexGrow: 1,
              p: { xs: 2, sm: 3 },
              width: '100%',
              minHeight: '100vh',
              backgroundColor: '#646464',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center'
            }}
          >
            <Toolbar />
            <Box sx={{ width: '100%', maxWidth: '1200px' }}>
              <Routes>
                <Route path="/bio" element={<Bio />} />
                <Route path="/about" element={<About />} />
                <Route path="/board" element={<Board sgfData={sgfData} setSgfData={setSgfData} />} />
                <Route path="/" element={<Navigate to="/bio" replace />} />
              </Routes>
            </Box>
          </Box>
        </Box>
      </Router>
    </>
  );
}

export default App