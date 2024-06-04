import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import { toast } from "react-toastify";
import { URL } from "../Config.js"
import './shisuan.css'

const Shisuan = (props) => {
  axios.defaults.baseURL = URL;
  const [bill, setBill] = useState({})
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('/uploadcsv/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setBill(response.data)
      console.log(response.data);
      alert('File uploaded successfully!');
    } catch (error) {
      console.error(error);
      alert('Error uploading file');
    }
  };
  return (
    <div className="shisuan-container">
      <Helmet>
        <title>shisuan - electricity</title>
        <meta property="og:title" content="shisuan - electricity" />
      </Helmet>
      <div className="shisuan-container1">
      
        <div className="shisuan-container2">
        <form onSubmit={handleSubmit}>
          <input
            type="file"
            placeholder=".csv"
            className="shisuan-textinput input"
            onChange={handleFileChange} 
          />
          <span className="shisuan-text">電表資料：</span>
          <span className="shisuan-text01">請上傳 .csv檔</span>
          <button type="submit" className="shisuan-button button">
            <span>
              <span className="shisuan-text03">試算</span>
              <br></br>
            </span>
          </button>
          </form>
        </div>
        
        <div className="shisuan-container3">
          <span className="shisuan-text05">{bill.usage}</span>
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
          <span className="shisuan-text15">{bill.bill_type1}</span>
          <span className="shisuan-text16">
            <span>{bill.bill_type2}</span>
            <br></br>
          </span>
          <span className="shisuan-text19">{bill.bill_type3}</span>
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
