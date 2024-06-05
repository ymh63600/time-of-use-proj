import React from 'react'
import { Link } from 'react-router-dom'

import { Helmet } from 'react-helmet'

import './nilm.css'

const Nilm = (props) => {
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
              src="/external/temp%20(8)-1500w-1500w.png"
              className="nilm-image pic"
            />
            <span className="nilm-text fenzhong">
              <span>14min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/external/temp%20(4)-1500w-1500w.png"
              className="nilm-image1 pic"
            />
            <span className="nilm-text03 fenzhong">
              <span>20min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/temp%20(11)-1500h.png"
              className="nilm-image2 pic"
            />
            <span className="nilm-text06 fenzhong">
              <span>46min(s)</span>
              <br></br>
            </span>
          </div>
          <div className="nilm-container4">
            <img
              alt="image"
              src="/external/temp%20(5)-1500w-1500w.png"
              className="nilm-image3 pic"
            />
            <span className="nilm-text09 fenzhong">
              <span>60min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/external/temp%20(10)-1500w-1500w.png"
              className="nilm-image4 pic"
            />
            <span className="nilm-text12 fenzhong">
              <span>35min(s)</span>
              <br></br>
            </span>
            <img
              alt="image"
              src="/external/temp%20(1)-1500w-1500w.png"
              className="nilm-image5 pic"
            />
            <span className="nilm-text15 fenzhong">
              <span>31min(s)</span>
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
