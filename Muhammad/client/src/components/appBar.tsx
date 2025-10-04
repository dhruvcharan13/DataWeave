import * as React from "react";
import {
  AppBar,
  Box,
  Toolbar,
  IconButton,
  Typography,
  Menu,
  Avatar,
  Button,
  Tooltip,
  MenuItem,
} from "@mui/material";
import AdbIcon from "@mui/icons-material/Adb";
import { useDispatch, useSelector } from "react-redux";
import { AppState } from "../store/appState";
import { uiActions, ThemeMode } from "../ui/slice";
import SettingsIcon from "@mui/icons-material/Settings";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";
import MenuIcon from "@mui/icons-material/Menu";
import { useRouter } from "next/router";
import styled from "styled-components";

const pages = [];
const themeOptions: ThemeMode[] = ["light", "dark"];

function ResponsiveAppBar() {
  const dispatch = useDispatch();
  const router = useRouter();

  const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(
    null
  );

  const [anchorElTheme, setAnchorElTheme] = React.useState<null | HTMLElement>(
    null
  );

  const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleOpenThemeMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorElTheme(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseThemeMenu = () => {
    setAnchorElTheme(null);
  };

  const handleThemeChange = (mode: ThemeMode) => {
    dispatch(uiActions.setThemeMode(mode));
  };

  const onClickRoute = (route: string) => {
    router.push(route);
    setAnchorElNav(null);
  };

  return (
    <AppBarWrapper position="static">
      <Toolbar disableGutters>
        <AdbIcon
          className="adb-icon"
          sx={{ display: { xs: "none", md: "flex" } }}
        />
        <Typography
          variant="h6"
          noWrap
          component="a"
          onClick={() => onClickRoute("/")}
          sx={{ display: { xs: "none", md: "flex" } }}
          className="logo-typography"
        >
          LOGO
        </Typography>

        <Box sx={{ flexGrow: 1, display: { xs: "flex", md: "none" } }}>
          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleOpenNavMenu}
            color="inherit"
          >
            <MenuIcon />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorElNav}
            anchorOrigin={{
              vertical: "bottom",
              horizontal: "left",
            }}
            keepMounted
            transformOrigin={{
              vertical: "top",
              horizontal: "left",
            }}
            open={Boolean(anchorElNav)}
            onClose={handleCloseNavMenu}
            sx={{ display: { xs: "block", md: "none" } }}
          >
            {pages.map((page) => (
              <MenuItem key={page} onClick={() => onClickRoute(page)}>
                <Typography sx={{ textAlign: "center" }}>{page}</Typography>
              </MenuItem>
            ))}
          </Menu>
        </Box>
        <AdbIcon sx={{ display: { xs: "flex", md: "none" }, mr: 1 }} />
        <Typography
          variant="h5"
          noWrap
          component="a"
          onClick={() => onClickRoute("/")}
          sx={{
            mr: 2,
            display: { xs: "flex", md: "none" },
            flexGrow: 1,
            fontFamily: "monospace",
            fontWeight: 700,
            letterSpacing: ".3rem",
            color: "inherit",
            textDecoration: "none",
          }}
        >
          LOGO
        </Typography>
        <Box sx={{ flexGrow: 1, display: { xs: "none", md: "flex" } }}>
          {pages.map((page) => (
            <Button
              key={page}
              onClick={() => onClickRoute(page)}
              sx={{ my: 2, color: "white", display: "block" }}
            >
              {page}
            </Button>
          ))}
        </Box>
        <Box sx={{ flexGrow: 0, p: 2 }}>
          <Tooltip title="Theme settings">
            <IconButton onClick={handleOpenThemeMenu}>
              <SettingsIcon />
            </IconButton>
          </Tooltip>
          <Menu
            id="menu-theme"
            anchorEl={anchorElTheme}
            anchorOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            keepMounted
            transformOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            open={Boolean(anchorElTheme)}
            onClose={handleCloseThemeMenu}
          >
            {themeOptions.map((themeOption) => (
              <MenuItem
                key={themeOption}
                onClick={() => {
                  handleThemeChange(themeOption);
                  handleCloseThemeMenu();
                }}
                sx={{
                  display: "flex",
                  gap: "10px",
                  alignItems: "center",
                  minHeight: "auto",
                  py: 1,
                  px: 2,
                }}
              >
                {themeOption === "light" ? (
                  <LightModeIcon sx={{ fontSize: "20px" }} />
                ) : (
                  <DarkModeIcon sx={{ fontSize: "20px" }} />
                )}
                <Typography textAlign="center">
                  {themeOption.charAt(0).toUpperCase() + themeOption.slice(1)}
                </Typography>
              </MenuItem>
            ))}
          </Menu>
        </Box>
      </Toolbar>
    </AppBarWrapper>
  );
}
export default ResponsiveAppBar;

const AppBarWrapper = styled(AppBar)`
  .adb-icon {
    margin: 0 16px;
  }

  .logo-typography {
    font-family: monospace;
    font-weight: 700;
    letter-spacing: 0.3rem;
    color: inherit;
    text-decoration: none;
    margin-right: 2rem;
  }
`;
