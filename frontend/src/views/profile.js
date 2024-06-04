import React,{useEffect,useState} from 'react'
import { Link ,useHistory} from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import {URL} from "../Config.js"
import './profile.css'
import {toast} from "react-toastify";

const Profile = (props) => {
  axios.defaults.baseURL = URL;
  const history = useHistory();
  const [getForm,setGetForm]=useState({
    electricity_meter:"",
  })
  const [user,setUser]=useState({})
    useEffect(()=>{
        const token=localStorage.getItem("auth_token")
        axios.get("/user/",{
            headers:{Authorization:token}
        }).then((response)=>{
            console.log(response)
            setUser(response.data)
            toast.success(response.data.detail)
        }).catch((error)=>{
            console.log(error.response.data.detail)
            toast.error(error.response.data.detail);
        })
    },[])
  const onChangeForm=(label,event)=>{
    switch(label){
        case "electricity_meter":
            setGetForm({...getForm,electricity_meter:event.target.value});
            break;
        default:
            break;
    }
  }
  const onSubmitHandler= async(event)=>{
    event.preventDefault()
    const token=localStorage.getItem("auth_token")
    await axios.patch("/user/",getForm,{headers:{Authorization:token}}).then((response)=>{
        toast.success("success!")
        history.push("/profile")  
        console.log(response)
    }).catch((error)=>{
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  
  const onClickHandler_LogOut = (event) => {
    event.preventDefault()
    localStorage.removeItem("auth_token")
    localStorage.removeItem("is_Admin")
    toast("See you !",{
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
  }
  return (
    <div className="profile-container">
      <Helmet>
        <title>profile - electricity</title>
        <meta property="og:title" content="profile - electricity" />
      </Helmet>
      <div className="profile-container1">
        <div className="profile-container2">
          <img
            alt="image"
            src="/frontend%20web%20(3)-1500w.png"
            className="profile-image"
          />
        </div>
        <div className="profile-container3">
        <form onSubmit={onSubmitHandler}>
          <input
            type="text"
            placeholder={user.electricity_meter}
            className="profile-textinput input"
            onChange={(event)=>{onChangeForm("electricity_meter",event)}}
          />
          <button type="submit" className="profile-button button">
            <span>
              <span className="profile-text07">Update</span>
              <br></br>
            </span>
          </button>
          </form>
          <Link to="/change-password" className="profile-navlink button">
            Change Password
          </Link>
          <Link to="/delete-account" className="profile-navlink1 button">
            <span className="profile-text">
              <span>Delete Account</span>
              <br></br>
            </span>
          </Link>
          <button type="button" className="profile-navlink2 button" onClick={onClickHandler_LogOut}>
            <span>
              <span>Logout</span>
              <br></br>
            </span>
          </button>
          <img alt="image" src="/email-1500w.png" className="profile-image1" />
          <img
            alt="image"
            src="/password-1500w.png"
            className="profile-image2"
          />
          <img alt="image" src="/logout-1500w.png" className="profile-image3" />
          <img
            alt="image"
            src="/delete%20acc-1500w.png"
            className="profile-image4"
          />
          <img
            alt="image"
            src="/dianbiao1-1000h.png"
            className="profile-image5"
          />
          
          <span className="profile-text09">
            <span>email</span>
            <br></br>
          </span>
        </div>
      </div>
      <header data-thq="thq-navbar" className="profile-navbar-interactive">
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="profile-image6"
        />
        <Link to="/profile" className="profile-navlink3 button">
          <img
            alt="image"
            src="/frontend%20web%20(5)-1500h.png"
            className="profile-image7"
          />
        </Link>
        <Link to="/home" className="profile-navlink4 button">
          <img
            alt="image"
            src="/frontend%20web%20(4)-1500h.png"
            className="profile-image8"
          />
        </Link>
      </header>
    </div>
  )
}

export default Profile
