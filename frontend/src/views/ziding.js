import React,{useEffect,useState} from 'react'
import { Link } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import {toast} from "react-toastify";
import './ziding.css'
import qs from 'qs';

const Ziding = (props) => {
  axios.defaults.baseURL = 'http://localhost:8000';
  const [daylimitForm,setDayLimitForm]=useState({
    daylimit:"",
  })
  const [monthlimitForm,setMonthLimitForm]=useState({
    monthlimit:"",
  })
  const [user,setUser]=useState({})
  const onChangeForm=(label,event)=>{
    switch(label){
        case "daylimit":
          setDayLimitForm({...daylimitForm,daylimit:event.target.value});
          
          break;
        case "monthlimit":
          setMonthLimitForm({...monthlimitForm,monthlimit:event.target.value});
          break;
        default:
            break;
    }
  }
  useEffect(()=>{
    const token=localStorage.getItem("auth_token")
    axios.get("/limit/",{
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
  const [usage,setUsage]=useState({})
  useEffect(()=>{
    const token=localStorage.getItem("auth_token")
    axios.get("/electricity/today/",{
        headers:{Authorization:token}
    }).then((response)=>{
        console.log(response)
        setUsage(response.data)
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error.response.data.detail)
        toast.error(error.response.data.detail);
    })
  },[])
  const [month_usage,setMonthUsage]=useState({})
  useEffect(()=>{
    const token=localStorage.getItem("auth_token")
    axios.get("/electricity/thismonth/",{
        headers:{Authorization:token}
    }).then((response)=>{
        console.log(response)
        setMonthUsage(response.data)
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error.response.data.detail)
        toast.error(error.response.data.detail);
    })
  },[])
  const now = new Date();
  const onDayClickHandler= async(event)=>{
    event.preventDefault()
    const token=localStorage.getItem("auth_token")
    console.log(daylimitForm)
    await axios.post("/limit/day/",daylimitForm,{
      headers:{Authorization:token,'Content-Type':'application/x-www-form-urlencoded'},data:qs.stringify({daylimit:daylimitForm.daylimit})
    }).then((response)=>{
        console.log(response)
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  const onMonthClickHandler= async(event)=>{
    event.preventDefault()
    const token=localStorage.getItem("auth_token")
    console.log(monthlimitForm)
    await axios.patch("/limit/month/",monthlimitForm,{
      headers:{Authorization:token,'Content-Type':'application/x-www-form-urlencoded'},data:qs.stringify({monthlimit:monthlimitForm.monthlimit})
      }).then((response)=>{
        console.log(response)
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error)
        toast.error(error.response.data.detail);
    })
  };
  return (
    <div className="ziding-container">
      <Helmet>
        <title>ziding - electricity</title>
        <meta property="og:title" content="ziding - electricity" />
      </Helmet>
      <img alt="image" src="/meiri-1500w.png" className="ziding-image" />
      <img alt="image" src="/meiyue-1500w.png" className="ziding-image1" />
      <img alt="image" src="/p1-1500w.png" className="ziding-image2" />
      <form onSubmit={onDayClickHandler}>
      <input 
        type="number" 
        placeholder={user.daylimit} 
        className="ziding-textinput input" 
        onChange={(event)=>{onChangeForm("daylimit",event)}} />
      <button type="submit" className="ziding-button button">
        <span className="ziding-text">
          <span>Update</span>
          <br></br>
        </span>
      </button>
      </form>
      <form onSubmit={onMonthClickHandler}>
      <input
        type="number"
        placeholder={user.monthlimit}
        className="ziding-textinput1 input"
        onChange={(event)=>{onChangeForm("monthlimit",event)}}
      />
      <button type="submit" className="ziding-button1 button">
        <span className="ziding-text03">
          <span>Update</span>
          <br></br>
        </span>
      </button>
      </form>
      <img alt="image" src="/p2-1500w.png" className="ziding-image3" />
      <span className="ziding-text06">{(parseFloat(month_usage.usage)/parseFloat(user.monthlimit)).toFixed(2)*100}%</span>
      <span className="ziding-text07">{(parseFloat(usage.usage)/parseFloat(user.daylimit)).toFixed(2)*100}%</span>
      <img alt="image" src="/mr1-1500w.png" className="ziding-image4" />
      <img alt="image" src="/my1-1500w.png" className="ziding-image5" />
      <header data-thq="thq-navbar" className="ziding-navbar-interactive">
        <Link to="/11" className="ziding-navlink button">
          <span>
            <span>&lt; Back</span>
            <br></br>
          </span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="ziding-image6"
        />
      </header>
      
      
    </div>
  )
}

export default Ziding
