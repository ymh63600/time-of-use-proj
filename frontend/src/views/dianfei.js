import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import { toast } from "react-toastify";
import { URL } from "../Config.js"
import './dianfei.css'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const Dianfei = (props) => {
  axios.defaults.baseURL = URL;
  const [user, setUser] = useState({})
  const [drawData, setData] = useState({})
  const [bill, setBill] = useState({})

  useEffect(() => {
    const token = localStorage.getItem("auth_token")
    axios.get("/calculate", {
      headers: { Authorization: token }
    }).then((response) => {
      console.log(response)
      setBill(response.data)
      toast.success(response.data.detail)
    }).catch((error) => {
      console.log(error.response.data.detail)
      toast.error(error.response.data.detail);
    })
  }, [])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("auth_token");
        const response = await axios.get("/fetch/timeUsage/", {
          headers: { Authorization: token }
        });
        console.log(response);
        setData(response.data);
        console.log(response.data.detail)
        toast.success(response.data.detail);
      } catch (error) {
        console.log(error.response.data.detail);
        toast.error(error.response.data.detail);
      }
    }
    fetchData();

  },)
  const mappedData = Array.isArray(drawData) ? drawData.map(item => {
    const time = item[0].split('T')[1];// 提取日期部分
    const hour = time.split(':')[0]
    const value = item[1];
    let value_rounded = parseFloat(value.toFixed(2));
    return { hour, value_rounded };
  }) : [];
  console.log(mappedData)
  const differences = mappedData.map((item, index) => {
    if (index === 0) {
      // 第一个元素没有前一项，差值设为0
      return { hour: item.hour, value: 0 };
    }
    const difference = item.value_rounded - mappedData[index - 1].value_rounded
    const value = parseFloat(difference.toFixed(2))
    return {
      hour: item.hour,
      value: value
    };
  });
  console.log(differences)
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
          <span className="dianfei-text09">{bill.bill_type1}</span>
          <span className="dianfei-text10">{bill.bill_type2}</span>
          <span className="dianfei-text13">{bill.bill_type3}</span>
          <span className="dianfei-text14">
            <span>上個月電費方案估價：</span>
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
          <LineChart
            width={500}
            height={300}
            data={differences}
            margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}
          >
            <CartesianGrid strokeDasharray="5 5" />
            <XAxis dataKey="hour" />
            <YAxis type="number" domain={[0, 'dataMax']} />
            <Tooltip />
            <Legend />
            <Line name="usage of eletricity" type="monotone" dataKey="value" stroke="#8884d8" activeDot={{ r: 6 }} />
          </LineChart>
          <span className="dianfei-text17">每小時用電度數 : </span>
        </div>

      </div>
    </div>
  )
}

export default Dianfei

