import React,{useState} from 'react'
import { Link,useHistory } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import {URL} from "../Config.js"
import './find-password.css'
import {toast} from "react-toastify";

const FindPassword = (props) => {
  axios.defaults.baseURL = URL;
  const history = useHistory();
  const [findPasswordForm,setFindPasswordForm]=useState({
    new_password:"",
    confirm_password:""
  })
  const changepage = () => {
    history.push('/'); 
  }
  const onChangeForm=(label,event)=>{
    switch(label){
        case "new_password":
            setFindPasswordForm({...findPasswordForm,new_password:event.target.value});
            break;
        case "confirm_password":
            setFindPasswordForm({...findPasswordForm,confirm_password:event.target.value});
            break;
        default:
            break;
    }
  }
  const onSubmitHandler= async()=>{
    const token=props.match.params.token
    await axios.post("/password/find/"+token,findPasswordForm).then((response)=>{ 
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
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  return (
    <div className="change-password-container">
      <Helmet>
        <title>reset-password - electricity</title>
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
              <span className="change-password-text1">Set</span>
              <br></br>
            </span>
          </button>
          </form>
          <button type="submit" className="change-password-button-2 button " onClick={changepage}>
            <span>
              <span className="change-password-text1">Login</span>
              <br></br>
            </span>
          </button>
          <img
            alt="image"
            src="/password-1500w.png"
            className="change-password-image1"
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
        
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="change-password-image4"
        />
      </header>
    </div>
  )
}

export default FindPassword
