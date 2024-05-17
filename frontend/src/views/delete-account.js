import React from 'react'
import { Link ,useHistory} from 'react-router-dom'
import axios from "axios"
import { Helmet } from 'react-helmet'
import { toast } from "react-toastify";
import {URL} from "../Config.js"
import './delete-account.css'

const DeleteAccount = (props) => {
  const history = useHistory();
  axios.defaults.baseURL = URL;
  const onDeleteHandler = async (event) => {
    event.preventDefault()
    const token = localStorage.getItem("auth_token")
    await axios.delete("/user/", { headers: { Authorization: token } }).then((response) => {
      toast("See you !", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined
      })
      setTimeout(() => {
        history.push("/")
      }, 1500)
    }).catch((error) => {
      toast.error(error.response.data.detail);
      console.log(error)
    })
  };
  return (
    <div className="delete-account-container">
      <Helmet>
        <title>delete-account - electricity</title>
        <meta property="og:title" content="delete-account - electricity" />
      </Helmet>
      <img
        alt="image"
        src="/frontend%20web%20(1)-1500w.png"
        className="delete-account-image"
      />
      <h1 className="delete-account-text">
        <span>Click to Confirm</span>
        <br></br>
      </h1>
      <button type="button" className="delete-account-button button" onClick={onDeleteHandler}>
        <span>
          <span>Delete Account</span>
          <br></br>
        </span>
      </button>
      <span className="delete-account-text05">
        <span>
          Are you sure
          <span
            dangerouslySetInnerHTML={{
              __html: ' ',
            }}
          />
        </span>
        <br></br>
        <span>you want to delete your account?</span>
        <br></br>
      </span>
      <header
        data-thq="thq-navbar"
        className="delete-account-navbar-interactive"
      >
        <Link to="/profile" className="delete-account-navlink1 button">
          <span>
            <span>&lt; Back</span>
            <br></br>
          </span>
        </Link>
        <img
          alt="image"
          src="/frontend%20web%20(2)-1500h.png"
          className="delete-account-image1"
        />
      </header>
    </div>
  )
}

export default DeleteAccount
