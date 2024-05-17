import React,{useState} from 'react'
import { Link } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import {URL} from "../Config.js"
import './forgot-password.css'
import {toast} from "react-toastify";

import './forgot-password.css'

const ForgotPassword = (props) => {
  axios.defaults.baseURL = URL;
  const [changeForm,setChangeForm]=useState({
    username:"",
  })
  const onChangeForm=(label,event)=>{
    switch(label){
        case "username":
            setChangeForm({...changeForm,username:event.target.value});
            break;
        default:
            break;
    }
  }
  const onSubmitHandler= async(event)=>{
    event.preventDefault()
    console.log(changeForm)
    await axios.patch("/password/forget/",changeForm).then((response)=>{
        console.log(response)
        localStorage.setItem("auth_token",response.data.token)
        toast.success("Email sent!")
    }).catch((error)=>{
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  return (
    <div className="forgot-password-container">
      <Helmet>
        <title>forgot-password - electricity</title>
        <meta property="og:title" content="forgot-password - electricity" />
      </Helmet>
      <div className="forgot-password-container1">
        <div className="forgot-password-container2">
          <img
            alt="image"
            src="/frontend%20web%20(3)-1500w.png"
            className="forgot-password-image"
          />
        </div>
        <div className="forgot-password-container3">
        <form onSubmit={onSubmitHandler}>
          <input
            type="email"
            placeholder="email"
            className="forgot-password-textinput input"
            onChange={(event)=>{onChangeForm("username",event)}}
          />
          <button type="submit" className="forgot-password-button button">
            <span>
              <span className="forgot-password-text2">Reset</span>
              <br></br>
            </span>
          </button>
        </form> 
          <img
            alt="image"
            src="/email-1500w.png"
            className="forgot-password-image1"
          />
          <p className="forgot-password-text">
            Please enter your email to reset password
          </p>
          
        </div>
      </div>
      <header
        data-thq="thq-navbar"
        className="forgot-password-navbar-interactive"
      >
        <Link to="/" className="forgot-password-navlink button">
          <span>
            <span>&lt; Back</span>
            <br></br>
          </span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="forgot-password-image2"
        />
      </header>
    </div>
  )
}

export default ForgotPassword
