import React,{useState} from 'react'
import { Link , useHistory } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import './create.css'
import URL from "../Config.js"
import {toast} from "react-toastify";

const Create = (props) => {
  axios.defaults.baseURL = 'http://localhost:8000';
  const history = useHistory();
  const [formRegister,setFormRegister]=useState({
    username:" ",
    password:" ",
    confirm_password:" ",
    electricity_meter:" "
  })
  const onChangeForm=(label,event)=>{
    switch(label){
        case "username":
            setFormRegister({...formRegister,username:event.target.value})
            break
        case "password":
            setFormRegister({...formRegister,password:event.target.value})
            break
        case "confirm_password":
            setFormRegister({...formRegister,confirm_password:event.target.value})
            break
        case "electricity_meter":
            setFormRegister({...formRegister,electricity_meter:event.target.value})
            break
        default:
            break;
    }
  }
  const onSubmitHandler = async (event)=>{
      event.preventDefault()
      const token=localStorage.getItem("auth_token")
      console.log(formRegister)
      await axios.post("/user/",formRegister,{headers:{Authorization:token}}).then((response)=>{
        toast.success(response.data.detail)  
        console.log(response)
        localStorage.setItem("auth_token",response.data.token)
          
          history.push('/signup-successful');
      }).catch((error)=>{
          console.log(error)
          toast.error(error.response.data.detail);
      })
  }
  return (
    <div className="create-container">
      <Helmet>
        <title>create - electricity</title>
        <meta property="og:title" content="create - electricity" />
      </Helmet>
      <div className="create-container1">
        <div className="create-container2">
          <img
            alt="image"
            src="/frontend%20web%20(3)-1500w.png"
            className="create-profile"
          />
        </div>
        <div className="create-container3">
        <form onSubmit={onSubmitHandler}>
          <input
            type="email"
            placeholder="email"
            className="create-input input"
            onChange={(event)=>{onChangeForm("username",event)}}
          />
          <input
            type="text"
            placeholder="電表編號"
            className="create-input1 input"
            onChange={(event)=>{onChangeForm("electricity_meter",event)}}
          />
          <input
            type="password"
            placeholder="Password"
            className="create-textinput input"
            onChange={(event)=>{onChangeForm("password",event)}}
          />
          <input
            type="password"
            placeholder="Confirm Password"
            className="create-textinput1 input"
            onChange={(event)=>{onChangeForm("confirm_password",event)}}
          />
          <img alt="image" src="/email-1500w.png" className="create-image" />
          <img
            alt="image"
            src="/password-1500w.png"
            className="create-image1"
          />
          <img
            alt="image"
            src="/dianbiao1-1000h.png"
            className="create-image2"
          />
          <img
            alt="image"
            src="/password-1500w.png"
            className="create-image3"
          />
          <button type="submit" className="create-button button">
            <span>
              <span className="create-text1">Create</span>
              <br></br>
            </span>
          </button>
        </form>
          
        </div>
      </div>
      <header data-thq="thq-navbar" className="create-navbar-interactive">
        <Link to="/" className="create-navlink button">
          <span>
            <span>&lt; Back</span>
            <br></br>
          </span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="create-image4"
        />
      </header>
    </div>
  )
}

export default Create
