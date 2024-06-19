import React from 'react';
import { AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemText } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import { styled } from '@mui/material/styles';

const drawerWidth = 240;

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  zIndex: theme.zIndex.drawer + 1,
  backgroundColor: '#4a4a4a', // Dark grey
}));

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
  },
}));

const StyledLink = styled(Link)({
  textDecoration: 'none',
  color: 'inherit',
});

function NavDrawer() {
  const location = useLocation();
  const currentPath = location.pathname;

  return (
    <>
      <StyledAppBar position="fixed">
        <Toolbar>
          <Typography variant="h6" noWrap>
            SGFication
          </Typography>
        </Toolbar>
      </StyledAppBar>
      <StyledDrawer variant="permanent">
        <Toolbar />
        <List>
          <ListItem button component={StyledLink} to="/" selected={currentPath === '/'}>
            <ListItemText primary="Home" />
          </ListItem>
          <ListItem button component={StyledLink} to="/about" selected={currentPath === '/about'}>
            <ListItemText primary="About" />
          </ListItem>
          <ListItem button component={StyledLink} to="/upload" selected={currentPath === '/upload'}>
            <ListItemText primary="Upload" />
          </ListItem>
          <ListItem button component={StyledLink} to="/board" selected={currentPath === '/board'}>
            <ListItemText primary="Board" />
          </ListItem>
        </List>
      </StyledDrawer>
    </>
  );
}

export default NavDrawer;
