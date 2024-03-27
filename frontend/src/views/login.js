import React,{useState} from 'react'
import { Link, useHistory } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import './login.css'
import {toast} from "react-toastify";
const Login = (props) => {
  
  axios.defaults.baseURL = 'http://localhost:8000'
  //axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded'
  const history = useHistory();
  const [loginForm,setLoginForm]=useState({
    username:"",
    password:""
  })
  const onChangeForm=(label,event)=>{
    switch(label){
        case "username":
            setLoginForm({...loginForm,username:event.target.value});
            break;
        case "password":
            setLoginForm({...loginForm,password:event.target.value});
            break;
        default:
            break;
    }
  }
  const onSubmitHandler= async(event)=>{
    event.preventDefault()
    console.log(loginForm)
    await axios.post("/login",loginForm).then((response)=>{
        console.log(response)
        localStorage.setItem("auth_token",response.data.token)
        localStorage.setItem("is_Admin",response.data.Admin)
        if(response.data.is_Admin){
          history.push('/adminpage1');
        }else{
          history.push('/home');
        }
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  return (
    <React.Fragment>
    <div className="login-container">
      <Helmet>
        <title>electricity</title>
        <meta property="og:title" content="electricity" />
      </Helmet>
      <div className="login-container1">
        <img
          alt="image"
          src="/frontend%20web-1500h.png"
          className="login-image"
        />
        <h1 className="login-text header">電力App</h1>
        <form onSubmit={onSubmitHandler}>
          <div>
            <input
              type="text"
              placeholder="email"
              className="login-textinput input"
              onChange={(event)=>{onChangeForm("username",event)}}
            />
            <input
              type="password"
              placeholder="password"
              className="login-input input"
              onChange={(event)=>{onChangeForm("password",event)}}
            />
          </div>
          
          <div>
            <button type="submit" className="login-navlink button">
              Log in
            </button>  
          </div>      
              
        </form>
        <Link to="/create" className="login-navlink1 button">
          <span>
            <span>Register</span>
            <br></br>
          </span>
        </Link>
        <Link to="/forgot-password" className="login-navlink2 button">
          Forgot Password
        </Link>
        
        
      </div>
    </div>
    </React.Fragment>
  )
}

export default Login
