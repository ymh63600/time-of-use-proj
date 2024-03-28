import React,{useState}  from 'react'
import { useHistory } from 'react-router-dom'
import { Helmet } from 'react-helmet'
import axios from "axios"
import './adminpage1.css'
import {toast} from "react-toastify";
import URL from "../Config.js"
import qs from 'qs';

const Adminpage1 = (props) => {
  axios.defaults.baseURL = 'http://localhost:8000';
  //axios.defaults.headers.post['Content-Type'] = 
  axios.defaults.headers.delete['Content-Type'] = 'application/x-www-form-urlencoded'
  const history = useHistory();
  const [getForm,setGetForm]=useState({
    username:"",
  })
  const [user,setUser]=useState({})
  const onChangeForm=(label,event)=>{
    switch(label){
        case "username":
            setGetForm({...getForm,username:event.target.value});
            break;
        default:
            break;
    }
  }
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
  const onSubmitHandler= async(event)=>{
    event.preventDefault()
    const token=localStorage.getItem("auth_token")
    const is_Admin=localStorage.getItem("is_Admin")
    await axios.post("/admin/",getForm,{headers:{Authorization:token,is_Admin:is_Admin,'Content-Type':'application/x-www-form-urlencoded'}}).then((response)=>{
      toast.success(response.data.detail)
      console.log(response)
      setUser(response.data)
    }).catch((error)=>{
        toast.error(error.response.data.detail);
        console.log(error)
    })
  };
  const onDeleteHandler= async(event)=>{
    event.preventDefault()
    const token=localStorage.getItem("auth_token")
    const is_Admin=localStorage.getItem("is_Admin")
    console.log(getForm)
    await axios.delete("/admin/",{headers:{Authorization:token,is_Admin:is_Admin},data:qs.stringify({username:getForm.username})},getForm).then((response)=>{ 
      console.log(response)
      toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  return (
    <div className="adminpage1-container">
      <Helmet>
        <title>adminpage1 - electricity</title>
        <meta property="og:title" content="adminpage1 - electricity" />
      </Helmet>
      <header data-thq="thq-navbar" className="adminpage1-navbar-interactive">
        <button to="/" className="adminpage1-navlink button" onClick={onClickHandler_LogOut}>
          <span>Logout &gt;</span>
        </button>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="adminpage1-image"
        />
      </header>
      <div className="adminpage1-container1">
      <form onSubmit={onSubmitHandler}  className="adminpage1-form">
        <input
          type="text"
          placeholder="Username"
          className="adminpage1-textinput input"
          onChange={(event)=>{onChangeForm("username",event)}}
        />
        <button type="submit" className="adminpage1-button1 button">
          <span className="adminpage1-text07">
            <span className="adminpage1-text08">Search</span>
            <br></br>
          </span>
        </button>
        </form>
        <span className="adminpage1-text01">Username:{user.username}</span>
          <span className="adminpage1-text02">電表編號:{user.electricity_meter}</span>
          <span className="adminpage1-text03">Last Login:{user.last_login}</span>
          <button type="submit" className="adminpage1-button button" onClick={onDeleteHandler}>
            <span className="adminpage1-text04">
              <span>Delete User</span>
              <br></br>
            </span>
          </button>
        
        
      </div>
    </div>
  )
}

export default Adminpage1
