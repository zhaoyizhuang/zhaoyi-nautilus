import axios from 'axios'
import Cookies from 'js-cookie'

const isProduction = process.env === 'production'

export default axios.create({
  baseURL: isProduction ? 'https://zhaoyi-nautilus.herokuapp.com/' : 'http://127.0.0.1:8000',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': Cookies.get('csrftoken')
  }
})
