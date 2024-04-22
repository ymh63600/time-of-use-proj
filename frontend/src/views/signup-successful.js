import React,{useState} from 'react'
import { Link } from 'react-router-dom'
import { Helmet } from 'react-helmet'
import axios from "axios"
import './signup-successful.css'
import URL from "../Config.js"
import {toast} from "react-toastify";

const SignupSuccessful = (props) => {
  axios.defaults.baseURL = 'http://localhost:8000';
  const onSubmitHandler = async (event)=>{
    event.preventDefault()
    const token=localStorage.getItem("auth_token")
    await axios.get("/user/resend/",{headers:{Authorization:token}}).then((response)=>{
        console.log(response)
        toast.success("Email resent!")
    }).catch((error)=>{
        console.log(token)
        console.log(error)
        toast.error(error.response.data.detail);
    })
  }
  return (
    <div className="signup-successful-container">
      <Helmet>
        <title>signup-successful - electricity</title>
        <meta property="og:title" content="signup-successful - electricity" />
      </Helmet>
      <img
        alt="image"
        src="/frontend%20web%20(1)-1500w.png"
        className="signup-successful-image"
      />
      <h1 className="signup-successful-text">
        <span>Please verify your email</span>
        <br></br>
      </h1>
      <button type="button" className="signup-successful-button button" onClick={onSubmitHandler}>
        <span>
          <span>Resend</span>
          <br></br>
        </span>
      </button>
      <p className="signup-successful-text06">Didn&apos;t receive the email?</p>
      <span className="signup-successful-text07">
        <span>You have Successfully signed up.</span>
        <br></br>
        <span>
          You&apos;re almost there.
          <span
            dangerouslySetInnerHTML={{
              __html: ' ',
            }}
          />
        </span>
        <br></br>
        <span>We sent an email to your mailbox. </span>
        <br></br>
      </span>
      <header
        data-thq="thq-navbar"
        className="signup-successful-navbar-interactive"
      >
        <Link to="/" className="signup-successful-navlink button">
          <span>
            <span>&lt; Login</span>
            <br></br>
          </span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="signup-successful-image1"
        />
      </header>
    </div>
  )
}

export default SignupSuccessful
