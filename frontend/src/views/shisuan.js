import React,{useState} from 'react'
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
      <header data-thq="thq-navbar" className="shisuan-navbar-interactive">
        <div data-thq="thq-navbar-nav" className="shisuan-desktop-menu"></div>
        <div data-thq="thq-burger-menu" className="shisuan-burger-menu">
          <svg viewBox="0 0 1024 1024" className="shisuan-icon">
            <path d="M128 554.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 298.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 810.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667z"></path>
          </svg>
        </div>
        <div data-thq="thq-mobile-menu" className="shisuan-mobile-menu">
          <div className="shisuan-nav">
            <div className="shisuan-top">
              <img
                alt="image"
                src="https://presentation-website-assets.teleporthq.io/logos/logo.png"
                className="shisuan-logo"
              />
              <div data-thq="thq-close-menu" className="shisuan-close-menu">
                <svg viewBox="0 0 1024 1024" className="shisuan-icon02">
                  <path d="M810 274l-238 238 238 238-60 60-238-238-238 238-60-60 238-238-238-238 60-60 238 238 238-238z"></path>
                </svg>
              </div>
            </div>
            <nav className="shisuan-links">
              <span className="shisuan-text">About</span>
              <span className="shisuan-text01">Features</span>
              <span className="shisuan-text02">Pricing</span>
              <span className="shisuan-text03">Team</span>
              <span className="shisuan-text04">Blog</span>
            </nav>
            <div className="shisuan-buttons">
              <button className="shisuan-login button">Login</button>
              <button className="button">Register</button>
            </div>
          </div>
          <div>
            <svg
              viewBox="0 0 950.8571428571428 1024"
              className="shisuan-icon04"
            >
              <path d="M925.714 233.143c-25.143 36.571-56.571 69.143-92.571 95.429 0.571 8 0.571 16 0.571 24 0 244-185.714 525.143-525.143 525.143-104.571 0-201.714-30.286-283.429-82.857 14.857 1.714 29.143 2.286 44.571 2.286 86.286 0 165.714-29.143 229.143-78.857-81.143-1.714-149.143-54.857-172.571-128 11.429 1.714 22.857 2.857 34.857 2.857 16.571 0 33.143-2.286 48.571-6.286-84.571-17.143-148-91.429-148-181.143v-2.286c24.571 13.714 53.143 22.286 83.429 23.429-49.714-33.143-82.286-89.714-82.286-153.714 0-34.286 9.143-65.714 25.143-93.143 90.857 112 227.429 185.143 380.571 193.143-2.857-13.714-4.571-28-4.571-42.286 0-101.714 82.286-184.571 184.571-184.571 53.143 0 101.143 22.286 134.857 58.286 41.714-8 81.714-23.429 117.143-44.571-13.714 42.857-42.857 78.857-81.143 101.714 37.143-4 73.143-14.286 106.286-28.571z"></path>
            </svg>
            <svg
              viewBox="0 0 877.7142857142857 1024"
              className="shisuan-icon06"
            >
              <path d="M585.143 512c0-80.571-65.714-146.286-146.286-146.286s-146.286 65.714-146.286 146.286 65.714 146.286 146.286 146.286 146.286-65.714 146.286-146.286zM664 512c0 124.571-100.571 225.143-225.143 225.143s-225.143-100.571-225.143-225.143 100.571-225.143 225.143-225.143 225.143 100.571 225.143 225.143zM725.714 277.714c0 29.143-23.429 52.571-52.571 52.571s-52.571-23.429-52.571-52.571 23.429-52.571 52.571-52.571 52.571 23.429 52.571 52.571zM438.857 152c-64 0-201.143-5.143-258.857 17.714-20 8-34.857 17.714-50.286 33.143s-25.143 30.286-33.143 50.286c-22.857 57.714-17.714 194.857-17.714 258.857s-5.143 201.143 17.714 258.857c8 20 17.714 34.857 33.143 50.286s30.286 25.143 50.286 33.143c57.714 22.857 194.857 17.714 258.857 17.714s201.143 5.143 258.857-17.714c20-8 34.857-17.714 50.286-33.143s25.143-30.286 33.143-50.286c22.857-57.714 17.714-194.857 17.714-258.857s5.143-201.143-17.714-258.857c-8-20-17.714-34.857-33.143-50.286s-30.286-25.143-50.286-33.143c-57.714-22.857-194.857-17.714-258.857-17.714zM877.714 512c0 60.571 0.571 120.571-2.857 181.143-3.429 70.286-19.429 132.571-70.857 184s-113.714 67.429-184 70.857c-60.571 3.429-120.571 2.857-181.143 2.857s-120.571 0.571-181.143-2.857c-70.286-3.429-132.571-19.429-184-70.857s-67.429-113.714-70.857-184c-3.429-60.571-2.857-120.571-2.857-181.143s-0.571-120.571 2.857-181.143c3.429-70.286 19.429-132.571 70.857-184s113.714-67.429 184-70.857c60.571-3.429 120.571-2.857 181.143-2.857s120.571-0.571 181.143 2.857c70.286 3.429 132.571 19.429 184 70.857s67.429 113.714 70.857 184c3.429 60.571 2.857 120.571 2.857 181.143z"></path>
            </svg>
            <svg
              viewBox="0 0 602.2582857142856 1024"
              className="shisuan-icon08"
            >
              <path d="M548 6.857v150.857h-89.714c-70.286 0-83.429 33.714-83.429 82.286v108h167.429l-22.286 169.143h-145.143v433.714h-174.857v-433.714h-145.714v-169.143h145.714v-124.571c0-144.571 88.571-223.429 217.714-223.429 61.714 0 114.857 4.571 130.286 6.857z"></path>
            </svg>
          </div>
        </div>
        <Link to="/dianfei" className="shisuan-navlink button">
          <span>&lt; Back</span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-200h.png"
          className="shisuan-image"
        />
      </header>
      <div className="shisuan-container1">
        <div className="shisuan-container2">
          <input
            type="file"
            placeholder=".csv"
            className="shisuan-textinput input"
          />
          <span className="shisuan-text06">電表資料：</span>
          <span className="shisuan-text07">請上傳 .csv檔</span>
        </div>
        <button type="submit" className="shisuan-button button">
          <span>
            <span className="shisuan-text09">試算</span>
            <br></br>
          </span>
        </button>
        <div className="shisuan-container3">
          <span className="shisuan-text11">320</span>
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="shisuan-image1"
          />
          <img
            alt="image"
            src="/unit%20blank-1500h.png"
            className="shisuan-image2"
          />
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="shisuan-image3"
          />
          <img
            alt="image"
            src="/select%20blank-1500h.png"
            className="shisuan-image4"
          />
          <span className="shisuan-text12">累進電價</span>
          <span className="shisuan-text13">
            <span>住商型簡易時間電價</span>
            <br></br>
            <span>（兩段式）</span>
          </span>
          <span className="shisuan-text17">
            <span>住商型簡易時間電價</span>
            <br></br>
            <span>（三段式）</span>
          </span>
          <span className="shisuan-text21">2750</span>
          <span className="shisuan-text22">
            <span>2500</span>
            <br></br>
          </span>
          <span className="shisuan-text25">2635</span>
          <span className="shisuan-text26">用電量：</span>
        </div>
      </div>
    </div>
  )
}

export default Shisuan
