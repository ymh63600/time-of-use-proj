import React,{useState} from 'react'
import { Link , useHistory } from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import './create.css'
import URL from "../Config.js"
import {toast} from "react-toastify";
const Create = (props) => {
  axios.defaults.baseURL = 'http://localhost:8000';
  const history = useHistory();
  const [formRegister,setFormRegister]=useState({
    username:" ",
    password:" ",
    confirm_password:" ",
    electricity_meter:" "
  })
  const onChangeForm=(label,event)=>{
    switch(label){
        case "username":
            setFormRegister({...formRegister,username:event.target.value})
            break
        case "password":
            setFormRegister({...formRegister,password:event.target.value})
            break
        case "confirm_password":
            setFormRegister({...formRegister,confirm_password:event.target.value})
            break
        case "electricity_meter":
            setFormRegister({...formRegister,electricity_meter:event.target.value})
            break
        default:
            break;
    }
  }
  const onSubmitHandler = async (event)=>{
      event.preventDefault()
      const token=localStorage.getItem("auth_token")
      console.log(formRegister)
      await axios.post("/user/",formRegister,{headers:{Authorization:token}}).then((response)=>{
        toast.success(response.data.detail)  
        console.log(response)
        localStorage.setItem("auth_token",response.data.token)
          
          history.push('/signup-successful');
      }).catch((error)=>{
          console.log(error)
          toast.error(error.response.data.detail);
      })
  }
  return (
    <React.Fragment>
    <div className="create-container">
      <Helmet>
        <title>create - electricity</title>
        <meta property="og:title" content="create - electricity" />
      </Helmet>
      <header data-thq="thq-navbar" className="create-navbar-interactive">
        <div data-thq="thq-navbar-nav" className="create-desktop-menu"></div>
        <div data-thq="thq-burger-menu" className="create-burger-menu">
          <svg viewBox="0 0 1024 1024" className="create-icon">
            <path d="M128 554.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 298.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667zM128 810.667h768c23.552 0 42.667-19.115 42.667-42.667s-19.115-42.667-42.667-42.667h-768c-23.552 0-42.667 19.115-42.667 42.667s19.115 42.667 42.667 42.667z"></path>
          </svg>
        </div>
        <div data-thq="thq-mobile-menu" className="create-mobile-menu">
          <div className="create-nav">
            <div className="create-top">
              <img
                alt="image"
                src="https://presentation-website-assets.teleporthq.io/logos/logo.png"
                className="create-logo"
              />
              <div data-thq="thq-close-menu" className="create-close-menu">
                <svg viewBox="0 0 1024 1024" className="create-icon02">
                  <path d="M810 274l-238 238 238 238-60 60-238-238-238 238-60-60 238-238-238-238 60-60 238 238 238-238z"></path>
                </svg>
              </div>
            </div>
            <nav className="create-links">
              <span className="create-text">About</span>
              <span className="create-text1">Features</span>
              <span className="create-text2">Pricing</span>
              <span className="create-text3">Team</span>
              <span className="create-text4">Blog</span>
            </nav>
            <div className="create-buttons">
              <button className="create-login button">Login</button>
              <button className="button">Register</button>
            </div>
          </div>
          <div>
            <svg viewBox="0 0 950.8571428571428 1024" className="create-icon04">
              <path d="M925.714 233.143c-25.143 36.571-56.571 69.143-92.571 95.429 0.571 8 0.571 16 0.571 24 0 244-185.714 525.143-525.143 525.143-104.571 0-201.714-30.286-283.429-82.857 14.857 1.714 29.143 2.286 44.571 2.286 86.286 0 165.714-29.143 229.143-78.857-81.143-1.714-149.143-54.857-172.571-128 11.429 1.714 22.857 2.857 34.857 2.857 16.571 0 33.143-2.286 48.571-6.286-84.571-17.143-148-91.429-148-181.143v-2.286c24.571 13.714 53.143 22.286 83.429 23.429-49.714-33.143-82.286-89.714-82.286-153.714 0-34.286 9.143-65.714 25.143-93.143 90.857 112 227.429 185.143 380.571 193.143-2.857-13.714-4.571-28-4.571-42.286 0-101.714 82.286-184.571 184.571-184.571 53.143 0 101.143 22.286 134.857 58.286 41.714-8 81.714-23.429 117.143-44.571-13.714 42.857-42.857 78.857-81.143 101.714 37.143-4 73.143-14.286 106.286-28.571z"></path>
            </svg>
            <svg viewBox="0 0 877.7142857142857 1024" className="create-icon06">
              <path d="M585.143 512c0-80.571-65.714-146.286-146.286-146.286s-146.286 65.714-146.286 146.286 65.714 146.286 146.286 146.286 146.286-65.714 146.286-146.286zM664 512c0 124.571-100.571 225.143-225.143 225.143s-225.143-100.571-225.143-225.143 100.571-225.143 225.143-225.143 225.143 100.571 225.143 225.143zM725.714 277.714c0 29.143-23.429 52.571-52.571 52.571s-52.571-23.429-52.571-52.571 23.429-52.571 52.571-52.571 52.571 23.429 52.571 52.571zM438.857 152c-64 0-201.143-5.143-258.857 17.714-20 8-34.857 17.714-50.286 33.143s-25.143 30.286-33.143 50.286c-22.857 57.714-17.714 194.857-17.714 258.857s-5.143 201.143 17.714 258.857c8 20 17.714 34.857 33.143 50.286s30.286 25.143 50.286 33.143c57.714 22.857 194.857 17.714 258.857 17.714s201.143 5.143 258.857-17.714c20-8 34.857-17.714 50.286-33.143s25.143-30.286 33.143-50.286c22.857-57.714 17.714-194.857 17.714-258.857s5.143-201.143-17.714-258.857c-8-20-17.714-34.857-33.143-50.286s-30.286-25.143-50.286-33.143c-57.714-22.857-194.857-17.714-258.857-17.714zM877.714 512c0 60.571 0.571 120.571-2.857 181.143-3.429 70.286-19.429 132.571-70.857 184s-113.714 67.429-184 70.857c-60.571 3.429-120.571 2.857-181.143 2.857s-120.571 0.571-181.143-2.857c-70.286-3.429-132.571-19.429-184-70.857s-67.429-113.714-70.857-184c-3.429-60.571-2.857-120.571-2.857-181.143s-0.571-120.571 2.857-181.143c3.429-70.286 19.429-132.571 70.857-184s113.714-67.429 184-70.857c60.571-3.429 120.571-2.857 181.143-2.857s120.571-0.571 181.143 2.857c70.286 3.429 132.571 19.429 184 70.857s67.429 113.714 70.857 184c3.429 60.571 2.857 120.571 2.857 181.143z"></path>
            </svg>
            <svg viewBox="0 0 602.2582857142856 1024" className="create-icon08">
              <path d="M548 6.857v150.857h-89.714c-70.286 0-83.429 33.714-83.429 82.286v108h167.429l-22.286 169.143h-145.143v433.714h-174.857v-433.714h-145.714v-169.143h145.714v-124.571c0-144.571 88.571-223.429 217.714-223.429 61.714 0 114.857 4.571 130.286 6.857z"></path>
            </svg>
          </div>
        </div>
        <Link to="/" className="create-navlink button">
          <span>&lt; Back</span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-200h.png"
          className="create-image"
        />
      </header>
      <div className="create-container1">
        <div className="create-container2">
          <img
            alt="image"
            src="/frontend%20web%20(3)-1500h.png"
            className="create-profile"
          />
        </div>
        <div className="create-container3">
        <form onSubmit={onSubmitHandler}>
          <input
            type="tel"
            placeholder="電表編號"
            className="create-textinput input"
            onChange={(event)=>{onChangeForm("electricity_meter",event)}}
          />
          <input
            type="tel"
            placeholder="Password"
            className="create-textinput1 input"
            onChange={(event)=>{onChangeForm("password",event)}}
          />
          <input
            type="tel"
            placeholder="Confirm Password"
            className="create-textinput2 input"
            onChange={(event)=>{onChangeForm("confirm_password",event)}}
          />
          <input
            type="email"
            placeholder="email"
            className="create-textinput3 input"
            onChange={(event)=>{onChangeForm("username",event)}}
          />
          <img alt="image" src="/email-1500h.png" className="create-image1" />
          <img
            alt="image"
            src="/password-1500h.png"
            className="create-image2"
          />
          <img
            alt="image"
            src="/dianbiao1-1500h.png"
            className="create-image3"
          />
          <img
            alt="image"
            src="/password-1500h.png"
            className="create-image4"
          />
          <button type="submit" className="create-button button">
            <span>
              <span className="create-text7">Create</span>
              <br></br>
            </span>
          </button>
        </form>
        </div>
      </div>
    </div>
    </React.Fragment>
  )
}

export default Create
