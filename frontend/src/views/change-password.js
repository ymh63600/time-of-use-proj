import React,{useState} from 'react'
import { Link,useHistory } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import URL from "../Config.js"
import './change-password.css'
import {toast} from "react-toastify";

const ChangePassword = (props) => {
  axios.defaults.baseURL = 'http://localhost:8000';
  
  const history = useHistory();
  const [loginForm,setLoginForm]=useState({
    current_password:"",
    new_password:"",
    confirm_password:""
  })
  const onChangeForm=(label,event)=>{
    switch(label){
        case "current_password":
            setLoginForm({...loginForm,current_password:event.target.value});
            break;
        case "new_password":
            setLoginForm({...loginForm,new_password:event.target.value});
            break;
        case "confirm_password":
            setLoginForm({...loginForm,confirm_password:event.target.value});
            break;
        default:
            break;
    }
  }
  const onSubmitHandler= async(event)=>{
    event.preventDefault()
    const token=localStorage.getItem("auth_token")
    await axios.patch("/password/update/",loginForm,{headers:{Authorization:token}}).then((response)=>{
      console.log(response)
      
      localStorage.removeItem("auth_token")
      toast("Enter your new password to login!",{
        position:"top-right",
        autoClose:5000,
        hideProgressBar:false,
        closeOnClick:true,
        pauseOnHover:true,
        draggable:true,
        progress:undefined
      })
      setTimeout(()=>{
        history.push("/")
      },1500)
    }).catch((error)=>{
      toast.error(error.response.data.detail);
        console.log(error)
    })
  };
  return (
    <div className="change-password-container">
      <Helmet>
        <title>change-password - electricity</title>
        <meta property="og:title" content="change-password - electricity" />
      </Helmet>
      <div className="change-password-container1">
        <div className="change-password-container2">
          <img
            alt="image"
            src="/frontend%20web%20(3)-1500w.png"
            className="change-password-image"
          />
        </div>
        <div className="change-password-container3">
        <form onSubmit={onSubmitHandler}>
          <input
            type="password"
            placeholder="Current Password"
            className="change-password-textinput input"
            onChange={(event)=>{onChangeForm("current_password",event)}}
          />
          <input
            type="password"
            placeholder="Password"
            className="change-password-textinput1 input"
            onChange={(event)=>{onChangeForm("new_password",event)}}
          />
          <input
            type="password"
            placeholder="Confirm Password"
            className="change-password-textinput2 input"
            onChange={(event)=>{onChangeForm("confirm_password",event)}}
          />
          <button type="submit" className="change-password-button button">
            <span>
              <span className="change-password-text1">Update</span>
              <br></br>
            </span>
          </button>
          </form>
          <img
            alt="image"
            src="/password-1500w.png"
            className="change-password-image1"
          />
          <img
            alt="image"
            src="/password-1500w.png"
            className="change-password-image2"
          />
          <img
            alt="image"
            src="/password-1500w.png"
            className="change-password-image3"
          />
          
        </div>
      </div>
      <header
        data-thq="thq-navbar"
        className="change-password-navbar-interactive"
      >
        <Link to="/profile" className="change-password-navlink button">
          <span>
            <span>&lt; Back</span>
            <br></br>
          </span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="change-password-image4"
        />
      </header>
    </div>
  )
}

export default ChangePassword
