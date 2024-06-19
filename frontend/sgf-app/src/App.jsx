import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CssBaseline, GlobalStyles, Box, Toolbar } from '@mui/material';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
// import NavTabs from './components/NavTabs';
import NavDrawer from './components/NavDrawer';
import About from './components/About';
import Upload from './components/Upload';
import Board from './components/Board';
import './App.css';


const globalStyles = (
  <GlobalStyles
    styles={{
      body: {
        backgroundColor: '#464646', // Off-white/silvery background
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

function Home({ count, setCount }) {
  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;