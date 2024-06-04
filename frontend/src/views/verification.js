import React,{useState} from 'react'
import axios from "axios"
import { Helmet } from 'react-helmet'
import { Link, useHistory } from 'react-router-dom'
import './verification.css'
import {URL} from "../Config.js"
import {toast} from "react-toastify";

const Verification = (props) => {
  axios.defaults.baseURL = URL;
  const history = useHistory();
  const change_page = () =>{
    history.push('/');
  }
  const onSubmitHandler= async()=>{
    const token=props.match.params.token
    await axios.get("/user/verification/"+token).then((response)=>{
        console.log(response)
        toast.success("success!")
    }).catch((error)=>{
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  onSubmitHandler()
  return (
    <div className="verification-container">
      <Helmet>
        <title>verification - electricity</title>
        <meta property="og:title" content="verification - electricity" />
      </Helmet>
      <img
        alt="image"
        src="/frontend%20web%20(1)-1500w.png"
        className="verification-image"
      />
      <h1 className="verification-text">
        <span>Verification Success</span>
        <br></br>
      </h1>
      <Link to="/" className="verification-navlink button">
        <span>
          <span>Login</span>
          <br></br>
        </span>
      </Link>
      <span className="verification-text06">
        <span>Thank you for your support.</span>
        <br></br>
        <span>Your email address was successfully verified.</span>
        <br></br>
      </span>
      <header data-thq="thq-navbar" className="verification-navbar-interactive">
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="verification-image1"
        />
      </header>
    </div>
  )
}

export default Verification
