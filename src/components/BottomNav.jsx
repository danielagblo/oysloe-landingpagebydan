import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import './BottomNav.css'
import homeIcon from '../assets/home.png'
import priceIcon from '../assets/price.png'
import registerIcon from '../assets/register.png'
import aboutIcon from '../assets/about.png'

const BottomNav = () => {
  const location = useLocation()
  
  const menuItems = [
    { name: 'Home', icon: homeIcon, path: '/' },
    { name: 'Pricing', icon: priceIcon, path: '/pricing' },
    { name: 'Register', icon: registerIcon, path: '/register' },
    { name: 'About', icon: aboutIcon, path: '/about' }
  ]

  return (
    <nav className="bottom-nav">
      {menuItems.map((item, index) => {
        const isActive = location.pathname === item.path
        return (
          <Link
            key={index}
            to={item.path}
            className={`nav-item ${isActive ? 'active' : ''}`}
          >
            <img src={item.icon} alt={item.name} className="nav-icon" />
            <span className="nav-label">{item.name}</span>
          </Link>
        )
      })}
    </nav>
  )
}

export default BottomNav

