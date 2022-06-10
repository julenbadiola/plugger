import { useAuth0 } from "@auth0/auth0-react";
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { Alert, Avatar, Box, Card, Container, Dialog, DialogContent, DialogTitle, Button, Grid, Stack, Typography, Stepper, Step, StepLabel, CardContent, CardMedia, CardHeader, CardActionArea } from '@mui/material';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { alpha, styled } from '@mui/material/styles';
import { useEffect, useState } from "react";
import __api__ from "../__api__";
import axios from 'axios';


const sameHeightCards = {
  minHeight: "50px",
  height: "100%",
  display: "flex",
  flexDirection: "column",
  justifyContent: "space-between"
}

const Asset = ({ asset }) => {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get(asset.plugin.urls.get.replace("{id}", asset.id || asset._id)).then(res => {
      setData(res.data)
    })
  }, [])

  return <CardActionArea onClick={() => window.open(asset.plugin.urls.view.replace("{id}", asset.id || asset._id), "_blank")}>
    {data && <Card style={sameHeightCards}>
      <CardHeader
        avatar={
          <Avatar src={data.icon} />
        }
        title={data.name}
        subheader={new Date(data.created_at).toLocaleDateString("es-ES", {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          timeZone: 'UTC'
        })}
      />


    </Card>}
  </CardActionArea>
}


const Home = () => {
  const {
    isAuthenticated,
  } = useAuth0();
  const [plugins, setPlugins] = useState([]);
  const [assets, setAssets] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedPlugin, setSelectedPlugin] = useState(null);

  // get plugins on init
  useEffect(() => {
    __api__.getPlugins().then((res) => {
      setPlugins(res)
    })
  }, [])

  // when plugins changed, get assets
  useEffect(() => {
    getAssets()
  }, [plugins])

  const getAssets = async () => {
    let allAssets = []
    for (const plugin of plugins) {
      const apiCall = await axios.get(plugin.urls.list)
      const enriched = apiCall.data.map(el => ({ ...el, plugin: plugin }))
      allAssets = [...allAssets, ...enriched]
    }
    setAssets(allAssets)
  }

  const handleClose = () => {
    setDialogOpen(false)
    setSelectedPlugin(null)
  }

  async function onMessage(event) {
    // Check sender origin to be trusted
    const { code, message } = event.data
    if (code === "asset_created") {
      handleClose()
      getAssets()
    }
  }

  useEffect(() => {
    // Initiate listeners
    if (window.addEventListener) {  // all browsers except IE before version 9
      window.addEventListener("message", onMessage, false);
    }
    else if (window.attachEvent) {
      window.attachEvent("onmessage", onMessage, false);
    }
    return () => {
      if (window.addEventListener) {
        window.removeEventListener("message", onMessage, false);
      }
      else if (window.attachEvent) {
        window.attachEvent("onmessage", onMessage, false);
      }
    }
  }, []);

  return (
    <Container maxWidth="lg">
      {isAuthenticated ? <Box sx={{ mt: 2 }}>
        <Typography variant="h5" sx={{ my: 3 }}>
          Current assets:
        </Typography>

        <Stack justifyContent="center">
          <Button variant="outlined" fullWidth onClick={() => setDialogOpen(true)}
            icon={<KeyboardArrowDownIcon />} color="primary">
            Create new
          </Button>
        </Stack>
        <Grid container spacing={3} sx={{ mt: 3 }}>

          {assets.length > 0 && assets.map(asset => <Grid item xs={3} key={asset.id || asset._id}>
            <Asset asset={asset} />
          </Grid>
          )}
        </Grid>
        {assets.length === 0 && <Alert fullWidth severity="info">There are no assets yet</Alert>
        }


        <Dialog
          open={dialogOpen}
          onClose={handleClose}
          aria-describedby="new-asset-dialog"
          maxWidth="lg"
          fullWidth
          sx={{ background: "main.default" }}
        >
          <DialogTitle>Create a new asset</DialogTitle>
          <DialogContent>
            <Stepper activeStep={selectedPlugin ? 1 : 0} alternativeLabel>
              <Step key={0}>
                <StepLabel>Select plugin</StepLabel>
              </Step>
              <Step key={1}>
                <StepLabel>Create asset</StepLabel>
              </Step>
            </Stepper>
            <Box sx={{ mt: 3 }}>
              {!selectedPlugin && <Grid container spacing={3}>
                {plugins.map(plugin => <Grid key={plugin.id} style={sameHeightCards} item xs={4} >
                  <CardActionArea onClick={() => setSelectedPlugin(plugin)}>
                    <Card>
                      <CardHeader
                        avatar={
                          <Avatar src={plugin.icon} />
                        }
                        title={plugin.name}
                      />
                      {plugin.snapshots && plugin.snapshots.length > 0 && <CardMedia
                        component="img"
                        height="194"
                        image={plugin.snapshots[0]}
                      />}
                      <CardContent>
                        <Typography variant="body2" color="text.secondary">
                          {plugin.description.substring(0, 200) + "..."}

                        </Typography>
                      </CardContent>
                    </Card>
                  </CardActionArea>
                </Grid>
                )}
              </Grid>}
              {selectedPlugin && <iframe frameborder="0" style={{ overflow: "hidden", height: "60vh", width: "100%" }} height="100%" width="100%" src={selectedPlugin && selectedPlugin.urls.instantiate} />}
            </Box>
          </DialogContent>
        </Dialog>
      </Box> : "You have to log in first"}
    </Container>
  )
};

export default Home;
