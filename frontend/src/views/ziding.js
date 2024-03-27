import React from 'react'
import { Link } from 'react-router-dom'

import { Helmet } from 'react-helmet'

import './ziding.css'

const Ziding = (props) => {
  return (
    <div className="ziding-container">
      <Helmet>
        <title>ziding - electricity</title>
        <meta property="og:title" content="ziding - electricity" />
      </Helmet>
      <img alt="image" src="/meiri-1500w.png" className="ziding-image" />
      <img alt="image" src="/meiyue-1500w.png" className="ziding-image1" />
      <img alt="image" src="/p1-1500w.png" className="ziding-image2" />
      <button type="button" className="ziding-button button">
        <span className="ziding-text">
          <span>Update</span>
          <br></br>
        </span>
      </button>
      <button type="button" className="ziding-button1 button">
        <span className="ziding-text03">
          <span>Update</span>
          <br></br>
        </span>
      </button>
      <img alt="image" src="/p2-1500w.png" className="ziding-image3" />
      <span className="ziding-text06">62%</span>
      <span className="ziding-text07">80%</span>
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
      <input type="number" placeholder="20" className="ziding-textinput input" />
      <input
        type="number"
        placeholder="200"
        className="ziding-textinput1 input"
      />
    </div>
  )
}

export default Ziding
