import React from 'react'
import { Link } from 'react-router-dom'

import { Helmet } from 'react-helmet'

import './shisuan.css'

const Shisuan = (props) => {
  return (
    <div className="shisuan-container">
      <Helmet>
        <title>shisuan - electricity</title>
        <meta property="og:title" content="shisuan - electricity" />
      </Helmet>
      <div className="shisuan-container1">
        <div className="shisuan-container2">
          <input
            type="file"
            placeholder=".csv"
            className="shisuan-textinput input"
          />
          <span className="shisuan-text">電表資料：</span>
          <span className="shisuan-text01">請上傳 .csv檔</span>
          <button type="submit" className="shisuan-button button">
            <span>
              <span className="shisuan-text03">試算</span>
              <br></br>
            </span>
          </button>
        </div>
        <div className="shisuan-container3">
          <span className="shisuan-text05">320</span>
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="shisuan-image"
          />
          <img
            alt="image"
            src="/unit%20blank-1500h.png"
            className="shisuan-image1"
          />
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="shisuan-image2"
          />
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="shisuan-image3"
          />
          <span className="shisuan-text06">累進電價</span>
          <span className="shisuan-text07">
            <span>住商型簡易時間電價</span>
            <br></br>
            <span>（兩段式）</span>
          </span>
          <span className="shisuan-text11">
            <span>住商型簡易時間電價</span>
            <br></br>
            <span>（三段式）</span>
          </span>
          <span className="shisuan-text15">2750</span>
          <span className="shisuan-text16">
            <span>2500</span>
            <br></br>
          </span>
          <span className="shisuan-text19">2635</span>
          <span className="shisuan-text20">用電量：</span>
        </div>
      </div>
      <header data-thq="thq-navbar" className="shisuan-navbar-interactive">
        <Link to="/dianfei" className="shisuan-navlink button">
          <span>
            <span>&lt; Back</span>
            <br></br>
          </span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="shisuan-image4"
        />
      </header>
    </div>
  )
}

export default Shisuan
