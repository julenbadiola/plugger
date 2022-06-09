import { useAuth0 } from "@auth0/auth0-react";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { Avatar, Box, Container, Dialog, DialogContent, DialogTitle, Fab, Stack, Typography } from '@mui/material';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { alpha, styled } from '@mui/material/styles';
import { useEffect, useState } from "react";
import __api__ from "../__api__";

const StyledMenu = styled((props) => (
  <Menu
    elevation={0}
    anchorOrigin={{
      vertical: 'bottom',
      horizontal: 'right',
    }}
    transformOrigin={{
      vertical: 'top',
      horizontal: 'right',
    }}
    {...props}
  />
))(({ theme }) => ({
  '& .MuiPaper-root': {
    borderRadius: 6,
    marginTop: theme.spacing(1),
    minWidth: 180,
    color:
      theme.palette.mode === 'light' ? 'rgb(55, 65, 81)' : theme.palette.grey[300],
    boxShadow:
      'rgb(255, 255, 255) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px',
    '& .MuiMenu-list': {
      padding: '4px 0',
    },
    '& .MuiMenuItem-root': {
      '& .MuiSvgIcon-root': {
        fontSize: 18,
        color: theme.palette.text.secondary,
        marginRight: theme.spacing(1.5),
      },
      '&:active': {
        backgroundColor: alpha(
          theme.palette.primary.main,
          theme.palette.action.selectedOpacity,
        ),
      },
    },
  },
}));

const Home = () => {
  const {
    isAuthenticated,
  } = useAuth0();
  const [anchorEl, setAnchorEl] = useState(null);
  const [plugins, setPlugins] = useState([]);
  const open = Boolean(anchorEl);

  const [dialogOpen, setDialogOpen] = useState(null);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  useEffect(() => {
    __api__.getPlugins().then((res) => {
      setPlugins(res)
    })
  }, [])

  return (
    <Container maxWidth="lg">
      {isAuthenticated ? <Box sx={{ mt: 2 }}>

        <Fab variant="extended" onClick={handleClick}
          icon={<KeyboardArrowDownIcon />} color="primary" sx={{
            position: 'fixed',
            top: 80,
            right: 16,
          }}>
          Start procedure
        </Fab>
        <StyledMenu
          id="demo-customized-menu"
          MenuListProps={{
            'aria-labelledby': 'demo-customized-button',
          }}
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
        >

          {plugins.map(plugin => <MenuItem key={plugin.name} onClick={() => setDialogOpen(plugin)}>
            <Stack spacing={2} alignItems="center" direction="row">
              <Avatar src={plugin.icon} /> <Typography variant="overline">{plugin.action_text}</Typography>
            </Stack>

          </MenuItem>)}
          <Dialog
            open={dialogOpen}
            onClose={() => setDialogOpen(false)}
            aria-describedby="new-asset-dialog"
            maxWidth="lg"
            fullWidth
            sx={{background: "main.default"}}
          >
            <DialogTitle>{"Create a new asset using"} { }</DialogTitle>
            <DialogContent>
              <iframe frameborder="0" style={{overflow: "hidden", height: "60vh", width: "100%"}} height="100%" width="100%" src={dialogOpen && dialogOpen.url + "/instantiate"} />
            </DialogContent>
          </Dialog>
        </StyledMenu>

      </Box> : "You have to log in first"}
    </Container>
  )
};

export default Home;
