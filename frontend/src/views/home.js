import React from 'react'
import { Link } from 'react-router-dom'

import { DateTimePrimitive } from '@teleporthq/react-components'
import { Helmet } from 'react-helmet'

import './home.css'

const Home = (props) => {
  return (
    <div className="home-container">
      <Helmet>
        <title>home - electricity</title>
        <meta property="og:title" content="home - electricity" />
      </Helmet>
      <div className="home-container1">
        <button type="button" className="home-button button">
          <Link to="/11">
            <img
              alt="image"
              src="/yongdian2-1000h.png"
              className="home-image"
            />
          </Link>
        </button>
        <button type="button" className="home-button1 button">
          <Link to="/dianfei">
            <img
              alt="image"
              src="/dianfei2-1000h.png"
              className="home-image1"
            />
          </Link>
        </button>
        <div className="home-container2">
          <img alt="image" src="/home1-1500w.png" className="home-image2" />
          <span className="home-date-time">
            <DateTimePrimitive
              format="MM.D.YYYY h:mm A"
              date="Mar 12 2024 22:52:51 GMT+0800"
            ></DateTimePrimitive>
          </span>
          <span className="home-text">今日用電量</span>
          <span className="home-text1">
            <span>12.50</span>
            <br></br>
          </span>
          <img alt="image" src="/home2-1500h.png" className="home-image3" />
        </div>
      </div>
      <header data-thq="thq-navbar" className="home-navbar-interactive">
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="home-image4"
        />
        <Link to="/profile" className="home-navlink2 button">
          <img
            alt="image"
            src="/frontend%20web%20(5)-1500h.png"
            className="home-image5"
          />
        </Link>
        <Link to="/home" className="home-navlink3 button">
          <img
            alt="image"
            src="/frontend%20web%20(4)-1500h.png"
            className="home-image6"
          />
        </Link>
      </header>
    </div>
  )
}

export default Home
