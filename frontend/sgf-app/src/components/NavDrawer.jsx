// NavDrawer.jsx
import React, { useState } from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Drawer, 
  IconButton, 
  List, 
  ListItem, 
  ListItemText,
  useMediaQuery 
} from '@mui/material';
import { Link, useLocation } from 'react-router-dom';
import { styled, useTheme } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';

const drawerWidth = 240;

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  zIndex: theme.zIndex.drawer + 1,
  backgroundColor: '#4a4a4a',
}));

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
    backgroundColor: theme.palette.background.default,
  },
}));

const StyledLink = styled(Link)({
  textDecoration: 'none',
  color: 'inherit',
});

function NavDrawer() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [mobileOpen, setMobileOpen] = useState(false); // Start closed on mobile
  const location = useLocation();
  const currentPath = location.pathname;

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const DrawerContent = (
    <>
      <Toolbar />
      <List>
        <ListItem button component={StyledLink} to="/bio" selected={currentPath === '/bio'}>
          <ListItemText primary="Bio" />
        </ListItem>
        <ListItem button component={StyledLink} to="/about" selected={currentPath === '/about'}>
          <ListItemText primary="About" />
        </ListItem>
        <ListItem button component={StyledLink} to="/board" selected={currentPath === '/board'}>
          <ListItemText primary="Board" />
        </ListItem>
      </List>
    </>
  );

  return (
    <>
      <StyledAppBar position="fixed">
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              {mobileOpen ? <CloseIcon /> : <MenuIcon />}
            </IconButton>
          )}
          <Typography variant="h6" noWrap>
            James <b>Andrew Taylor</b>
          </Typography>
        </Toolbar>
      </StyledAppBar>

      {isMobile ? (
        <StyledDrawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better mobile performance
          }}
          sx={{
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {DrawerContent}
        </StyledDrawer>
      ) : (
        <StyledDrawer
          variant="permanent"
          sx={{
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {DrawerContent}
        </StyledDrawer>
      )}
    </>
  );
}

export default NavDrawer;