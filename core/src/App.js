import { useAuth0 } from "@auth0/auth0-react";
import React, { useEffect } from "react";
import { Route, Router, Switch } from "react-router-dom";
import "./App.css";
import Layout from "./components/Layout";
import Loading from "./components/Loading";
import useStore from "./state";
import history from "./utils/history";
import Home from "./views/Home";

const App = () => {
  const {
    isLoading,
    error,
    user,
    getAccessTokenSilently
  } = useAuth0();

  useEffect(async () => {
    if (!isLoading) {
      if(user){
        const token = await getAccessTokenSilently();
        initialize(token)
        setEndpoints()
      }
      
    }
  }, [isLoading, user])

  if (error) {
    return <div>Oops... {error.message}</div>;
  }

  if (isLoading) {
    return <Loading />;
  }

  return (

    <Router history={history}>
      <div id="app">
        <Layout>
          <Switch>
            <Route path="/" exact component={Home} />
          </Switch>
        </Layout>
      </div>
    </Router>
  );
};

export default App;
