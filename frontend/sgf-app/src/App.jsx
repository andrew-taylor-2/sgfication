
import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline, GlobalStyles, Box, Toolbar } from '@mui/material';
import NavDrawer from './components/NavDrawer';
import About from './components/About';
import Upload from './components/Upload';
import Board from './components/Board';
import Home from './components/Home'; // Import your Home component
import './App.css';

// Global styles
const globalStyles = (
  <GlobalStyles
    styles={{
      body: {
        backgroundColor: '#f0f0f0', // Off-white/silvery background
        margin: 0,
        padding: 0,
        fontFamily: 'Roboto, sans-serif',
      },
    }}
  />
);

function App() {
  const [sgfData, setSgfData] = useState(null);
  const [count, setCount] = useState(0);

  return (
    <>
      <CssBaseline />
      {globalStyles}
      <Router>
        <NavDrawer />
        <Box component="main" sx={{ flexGrow: 1, p: 3, marginLeft: '240px' }}>
          <Toolbar />
          <Routes>
            <Route path="/about" element={<About />} />
            <Route path="/upload" element={<Upload setSgfData={setSgfData} />} />
            <Route path="/board" element={<Board sgfData={sgfData} />} />
            <Route path="/" element={<Home count={count} setCount={setCount} />} />
          </Routes>
        </Box>
      </Router>
    </>
  );
}

export default App;
