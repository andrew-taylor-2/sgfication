// src/components/NavTabs.jsx

import React from 'react';
import { AppBar, Tabs, Tab } from '@mui/material';
import { styled } from '@mui/material/styles';
import { Link, useLocation } from 'react-router-dom';

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  backgroundColor: '#4a4a4a', // Dark grey
  width: '100%',
}));

const StyledTabs = styled(Tabs)(({ theme }) => ({
  flexGrow: 1,
  justifyContent: 'center',
}));

const StyledTab = styled(Tab)(({ theme }) => ({
  color: '#ffffff', // White text
  minWidth: '100px', // Minimum width for tabs
  flexGrow: 1, // Tabs will grow to fill the space
}));

function NavTabs() {
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <StyledAppBar position="static">
      <StyledTabs value={currentPath} variant="fullWidth">
        <StyledTab label="Home" value="/" component={Link} to="/" />
        <StyledTab label="About" value="/about" component={Link} to="/about" />
        <StyledTab label="Upload" value="/upload" component={Link} to="/upload" />
        <StyledTab label="Board" value="/board" component={Link} to="/board" />
      </StyledTabs>
    </StyledAppBar>
  );
}

export default NavTabs;
