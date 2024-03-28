import React from 'react'
import { Link } from 'react-router-dom'

import { Helmet } from 'react-helmet'

import './dianfei.css'

const Dianfei = (props) => {
  return (
    <div className="dianfei-container">
      <Helmet>
        <title>dianfei - electricity</title>
        <meta property="og:title" content="dianfei - electricity" />
      </Helmet>
      <header data-thq="thq-navbar" className="dianfei-navbar-interactive">
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="dianfei-image"
        />
        <Link to="/profile" className="dianfei-navlink button">
          <img
            alt="image"
            src="/frontend%20web%20(5)-1500h.png"
            className="dianfei-image1"
          />
        </Link>
        <Link to="/home" className="dianfei-navlink1 button">
          <img
            alt="image"
            src="/frontend%20web%20(4)-1500h.png"
            className="dianfei-image2"
          />
        </Link>
      </header>
      <div className="dianfei-container1">
        <div className="dianfei-container2">
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="dianfei-image3"
          />
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="dianfei-image4"
          />
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="dianfei-image5"
          />
          <span className="dianfei-text">累進電價</span>
          <span className="dianfei-text01">
            <span>住商型簡易時間電價</span>
            <br></br>
            <span>（兩段式）</span>
          </span>
          <span className="dianfei-text05">
            <span>住商型簡易時間電價</span>
            <br></br>
            <span>（三段式）</span>
          </span>
          <span className="dianfei-text09">2750</span>
          <span className="dianfei-text10">
            <span>2500</span>
            <br></br>
          </span>
          <span className="dianfei-text13">2635</span>
          <span className="dianfei-text14">
            <span>方案估價：</span>
            <br></br>
          </span>
          <button type="button" className="dianfei-button button">
            <Link to="/shisuan">
              <img
                alt="image"
                src="/shisuan-1500h.png"
                className="dianfei-image6"
              />
            </Link>
          </button>
        </div>
        <div className="dianfei-container3">
          <img alt="image" src="/graph2-1500h.png" className="dianfei-image7" />
          <input
            type="date"
            placeholder="placeholder"
            className="dianfei-textinput input"
          />
          <select autoComplete="off" className="dianfei-select">
            <option value="Option 1">累進</option>
            <option value="00:00 - 03:00">二段式</option>
            <option value="Option 2">三段式</option>
          </select>
          <span className="dianfei-text17">選擇方案：</span>
        </div>
      </div>
    </div>
  )
}

export default Dianfei
