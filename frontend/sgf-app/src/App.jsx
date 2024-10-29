import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { CssBaseline, GlobalStyles, Box, Toolbar } from '@mui/material';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
// import NavTabs from './components/NavTabs';
import NavDrawer from './components/NavDrawer';
import About from './components/About';
import Bio from './components/Bio';
import Board from './components/Board';
import './App.css';


const globalStyles = (
  <GlobalStyles
    styles={{
      body: {
        backgroundColor: '#646464',//'#464646', // Off-white/silvery background
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
          <Route path="/bio" element={<Bio />} />
          <Route path="/about" element={<About />} />
          <Route path="/board" element={<Board sgfData={sgfData} setSgfData={setSgfData} />} />
          <Route path="/" element={<Navigate to="/bio" replace />} />
        </Routes>
        </Box>
      </Router>
    </>
  );
}

export default App;