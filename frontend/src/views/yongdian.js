import React, {useEffect,useState} from 'react'
import { Link } from 'react-router-dom'
import axios from "axios"
import { DateTimePrimitive } from '@teleporthq/react-components'
import { Helmet } from 'react-helmet'
import {toast} from "react-toastify";
import './yongdian.css'

const Yongdian = (props) => {
  axios.defaults.baseURL = 'http://localhost:8000';
  const [usage,setUsage]=useState({})
  const [rank,setRank]=useState({})
  useEffect(()=>{
    const token=localStorage.getItem("auth_token")
    axios.get("/electricity/lastmonth/",{
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
  useEffect(()=>{
    const token=localStorage.getItem("auth_token")
    axios.get("/electricity/compare/",{
        headers:{Authorization:token}
    }).then((response)=>{
        console.log(response)
        setRank(response.data)
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error.response.data.detail)
        toast.error(error.response.data.detail);
    })
  },[])
  const now = new Date();
  const carbon_emission = 0.495
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
    <div className="yongdian-container">
      <Helmet>
        <title>yongdian - electricity</title>
        <meta property="og:title" content="yongdian - electricity" />
      </Helmet>
      <div className="yongdian-container1">
        <div className="yongdian-container2">
          <img alt="image" src="/graph1-1500h.png" className="yongdian-image" />
          <img
            alt="image"
            src="/navigation%20bar-1500h.png"
            className="yongdian-image1"
          />
          <button type="button" className="yongdian-button button">
            <span>
              <span>  </span>
              <br></br>
              <br></br>
            </span>
          </button>
          <button type="button" className="yongdian-button1 button">
            <span>
              <span>  </span>
              <br></br>
              <br></br>
            </span>
          </button>
          <button type="button" className="yongdian-button2 button">
            <span>
              <span>  </span>
              <br></br>
              <br></br>
            </span>
          </button>
          <button type="button" className="yongdian-button3 button">
            <span>
              <span>  </span>
              <br></br>
              <br></br>
            </span>
          </button>
        </div>
        <div className="yongdian-container3">
          
          <span className="yongdian-text16">
            上月用電量在當前區域為多於{(parseFloat(rank.rank)*100).toFixed(0)}%人
          </span>
          <img alt="image" src="/jifei-1500w.png" className="yongdian-image2" />
          <span className="yongdian-text17">{(parseFloat(usage.usage) * carbon_emission).toFixed(2)}</span>
          <span className="yongdian-date-time">
            <DateTimePrimitive
              format="YYYY/MM/DD"
              date="Thu Mar 14 2024 15:04:38 GMT+0800 (Taipei Standard Time)"
            ></DateTimePrimitive>
          </span>
          <button type="button" className="yongdian-button4 button">
            <Link to="/ziding" className="yongdian-navlink">
              <img
                alt="image"
                src="/ziding-1000h.png"
                className="yongdian-image3"
              />
            </Link>
          </button>
          <form onSubmit={onSubmitHandler}>
          <input
            type="text"
            placeholder="年/月/日"
            className="yongdian-textinput1 input"
          />
          <button type="submit" className="yongdian-button5 button">
            <span>
                Update
            </span>
          </button>
          </form>
        </div>
      </div>
      <header data-thq="thq-navbar" className="yongdian-navbar-interactive">
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="yongdian-image4"
        />
        <Link to="/profile" className="yongdian-navlink2 button">
          <img
            alt="image"
            src="/frontend%20web%20(5)-1500h.png"
            className="yongdian-image5"
          />
        </Link>
        <Link to="/home" className="yongdian-navlink3 button">
          <img
            alt="image"
            src="/frontend%20web%20(4)-1500h.png"
            className="yongdian-image6"
          />
        </Link>
      </header>
    </div>
  )
}

export default Yongdian
