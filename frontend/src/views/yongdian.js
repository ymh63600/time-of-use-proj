import React from 'react'
import { Link } from 'react-router-dom'

import { DateTimePrimitive } from '@teleporthq/react-components'
import { Helmet } from 'react-helmet'

import './yongdian.css'

const Yongdian = (props) => {
  return (
    <div className="yongdian-container">
      <Helmet>
        <title>yongdian - electricity</title>
        <meta property="og:title" content="yongdian - electricity" />
      </Helmet>
      <div className="yongdian-container1">
        <div className="yongdian-container2">
          <img alt="image" src="/graph1-1500h.png" className="yongdian-image" />
          <input
            type="date"
            placeholder="placeholder"
            className="yongdian-textinput input"
          />
          <select className="yongdian-select">
            <option value="00:00 - 03:00">00:00 - 03:00</option>
            <option value="03:00 - 06:00">03:00 - 06:00</option>
            <option value="06:00 - 09:00">06:00 - 09:00</option>
            <option value="09:00 - 12:00">09:00 - 12:00</option>
            <option value="12:00 - 15:00">12:00 - 15:00</option>
            <option value="15:00 - 18:00">15:00 - 18:00</option>
            <option value="18:00 - 21:00">18:00 - 21:00</option>
            <option value="21:00 - 24:00">21:00 - 24:00</option>
          </select>
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
          <input
            type="date"
            placeholder="placeholder"
            className="yongdian-textinput1 input"
          />
          <span className="yongdian-text16">
            上月用電量在當前區域為多於97%人
          </span>
          <img alt="image" src="/jifei-1500w.png" className="yongdian-image2" />
          <span className="yongdian-text17">320</span>
          <span className="yongdian-date-time">
            <DateTimePrimitive
              format="DD/MM/YYYY"
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
        </div>
      </div>
      <header data-thq="thq-navbar" className="yongdian-navbar-interactive">
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="yongdian-image4"
        />
        <Link to="/profile" className="yongdian-navlink1 button">
          <img
            alt="image"
            src="/frontend%20web%20(5)-1500h.png"
            className="yongdian-image5"
          />
        </Link>
        <Link to="/home" className="yongdian-navlink2 button">
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
