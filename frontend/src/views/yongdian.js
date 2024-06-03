import React, {useEffect,useState} from 'react'
import { Link } from 'react-router-dom'
import axios from "axios"
import { DateTimePrimitive } from '@teleporthq/react-components'
import { Helmet } from 'react-helmet'
import {toast} from "react-toastify";
import {URL} from "../Config.js"
import './yongdian.css'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts';

const Yongdian = (props) => {
  axios.defaults.baseURL = URL;
  const [usage,setUsage]=useState({})
  const [rank,setRank]=useState({})
  const [drawData, setData]=useState({})
  
  useEffect(()=>{
    const token=localStorage.getItem("auth_token")
    axios.get("/electricity/lastmonth/",{
        headers:{Authorization:token}
    }).then((response)=>{
        console.log(response)
        setUsage(response.data)
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error.response.data.detail)
        toast.error(error.response.data.detail);
    })
  },[])
  useEffect(()=>{
    const token=localStorage.getItem("auth_token")
    axios.get("/electricity/compare/",{
        headers:{Authorization:token}
    }).then((response)=>{
        console.log(response)
        setRank(response.data)
        toast.success(response.data.detail)
    }).catch((error)=>{
        console.log(error.response.data.detail)
        toast.error(error.response.data.detail);
    })
  },[])
  const now = new Date();
  const carbon_emission = 0.495
  const onSubmitHandler= async(event)=>{
    
  };
  useEffect(()=>{
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("auth_token");
        const response = await axios.get("/fetch/timeUsage/", {
          headers:{Authorization:token}
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
    const time = item[0].split('T')[1]; // 提取日期部分//
    const hour = time.split(':')[0];
    const value = item[1];
    let value_rounded = parseFloat(value.toFixed(2));
    return { hour, value_rounded};
  }) : [];
  console.log(mappedData)
  const differences = mappedData.map((item, index) => {
  if (index === 0) {
    // 第一个元素没有前一项，差值设为0
    return { hour: item.hour, value: 0 };
  }
  const difference = item.value_rounded - mappedData[0].value_rounded
  const value = parseFloat(difference.toFixed(2))
  return {
    hour: item.hour,
    value : value
  };
  });
  console.log(differences)
  return (
    <div className="yongdian-container">
      <Helmet>
        <title>yongdian - electricity</title>
        <meta property="og:title" content="yongdian - electricity" />
      </Helmet>
      <div className="yongdian-container1">
        
        <LineChart
              width={700}
              height={300}
              data={differences}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
	    <CartesianGrid strokeDasharray="10 10" />
            <XAxis dataKey="hour"/>
            <YAxis type="number" domain={([dataMin, dataMax]) => { const absMax = Math.round(dataMax+1); return [0, absMax]; }}/>
            <Tooltip />
            <Legend />
            <Line name = "usage of eletricity"type="monotone" dataKey="value" stroke="#7CCD7C" activeDot={{ r: 8 }} />
	    </LineChart>
        <div className="yongdian-container3">
          
          <span className="yongdian-text16">
            上月用電量在當前區域為多於{(parseFloat(rank.rank)*100).toFixed(0)}%人
          </span>
          <img alt="image" src="/jifei-1500w.png" className="yongdian-image2" />
          <span className="yongdian-text17">{(parseFloat(usage.usage) * carbon_emission).toFixed(2)}</span>
          <span className="yongdian-date-time">
            <DateTimePrimitive
              format="YYYY/MM/DD"
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
          <form onSubmit={onSubmitHandler}>
          <input
            type="text"
            placeholder="年/月/日"
            className="yongdian-textinput1 input"
          />
          <button type="submit" className="yongdian-button5 button">
            <span>
                Update
            </span>
          </button>
          </form>
        </div>
      </div>
      <header data-thq="thq-navbar" className="yongdian-navbar-interactive">
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="yongdian-image4"
        />
        <Link to="/profile" className="yongdian-navlink2 button">
          <img
            alt="image"
            src="/frontend%20web%20(5)-1500h.png"
            className="yongdian-image5"
          />
        </Link>
        <Link to="/home" className="yongdian-navlink3 button">
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
