import React,{useState,useEffect} from 'react';
import ReactDOM from 'react-dom'

import {
  BrowserRouter as Router,
  Route,
  Switch,
  Redirect,
} from 'react-router-dom'

import './style.css'
import Shisuan from './views/shisuan'
import Create from './views/create'
import Dianfei from './views/dianfei'
import Yongdian from './views/yongdian'
import Ziding from './views/ziding'
import Verification from './views/verification'
import Adminpage1 from './views/adminpage1'
import ForgotPassword from './views/forgot-password'
import FindPassword from './views/find-password'
import SignupSuccessful from './views/signup-successful'
import Profile from './views/profile'
import ChangePassword from './views/change-password'
import Login from './views/login'
import Home from './views/home'
import NotFound from './views/not-found'
import {ToastContainer} from "react-toastify";
import "react-toastify/ReactToastify.min.css";

const App = () => {
  return (
    
    <Router>
      <ToastContainer/>
      <Switch>
        <Route component={Shisuan} exact path="/shisuan" />
        <Route component={Create} exact path="/create" />
        <Route component={Dianfei} exact path="/dianfei" />
        <Route component={Yongdian} exact path="/11" />
        <Route component={Ziding} exact path="/ziding" />
        <Route component={Verification} path="/verification/:token" />
        <Route component={Adminpage1} exact path="/adminpage1" />
        <Route component={ForgotPassword} exact path="/forgot-password" />
        <Route component={FindPassword} path="/find-password/:token" />
        <Route component={SignupSuccessful} exact path="/signup-successful" />
        <Route component={Profile} exact path="/profile" />
        <Route component={ChangePassword} exact path="/change-password" />
        <Route component={Login} exact path="/" />
        <Route component={Home} exact path="/home" />
        <Route component={NotFound} path="**" />
        <Redirect to="**" />
      </Switch>
    </Router>
    
  )
}

ReactDOM.render(<App />, document.getElementById('app'))

