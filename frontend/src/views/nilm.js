import React,{useEffect,useState} from 'react'
import axios from "axios"
import { Helmet } from 'react-helmet'
import { Link } from 'react-router-dom'

import './nilm.css'

const Nilm = (props) => {
  const [usage,setUsage]=useState({})
    useEffect(()=>{
        axios.get("http://localhost:8000/accumulate/").then((response)=>{
            console.log(response)
            setUsage(response.data)
        }).catch((error)=>{
            console.log(error.response.data.detail)
        })
    },[])
  return (
    <div className="nilm-container">
      <Helmet>
        <title>nilm - electricity</title>
        <meta property="og:title" content="nilm - electricity" />
      </Helmet>
      <div className="nilm-container1">
        <div className="nilm-container2">
          <div className="nilm-container3">
          <img
              alt="image"
              src="/temp%20(8)-1500w.png"
              className="nilm-image pic"
            />
            <span className="nilm-text fenzhong">
              <span>{usage.sockets}min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/temp%20(4)-1500w.png"
              className="nilm-image1 pic"
            />
            <span className="nilm-text03 fenzhong">
              <span>{usage.microwave}min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/temp%20(11).png"
              className="nilm-image2 pic"
            />
            <span className="nilm-text06 fenzhong">
              <span>{usage.light}min(s)</span>
              <br></br>
            </span>
          </div>
          <div className="nilm-container4">
            <img
              alt="image"
              src="/temp%20(5)-1500w.png"
              className="nilm-image3 pic"
            />
            <span className="nilm-text09 fenzhong">
              <span>{usage.fridge}min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/temp%20(10)-1500w.png"
              className="nilm-image4 pic"
            />
            <span className="nilm-text12 fenzhong">
              <span>{usage.electric_oven}min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/temp%20(1)-1500w.png"
              className="nilm-image5 pic"
            />
            <span className="nilm-text15 fenzhong">
              <span>{usage.dish_washer}min(s)</span>
              <br></br>
            </span>
          </div>
        </div>
        <header data-thq="thq-navbar" className="nilm-navbar-interactive">
          <Link to="/11" className="nilm-navlink button">
            <span>
              <span>&lt; Back</span>
              <br></br>
            </span>
          </Link>
          <img
            alt="image"
            src="/frontend%20web%20(8)-1500h.png"
            className="nilm-image6"
          />
        </header>
      </div>
    </div>
  )
}

export default Nilm
