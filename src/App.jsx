import React from 'react'
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import { RegistrationProvider } from './context/RegistrationContext'
import Home from './pages/Home'
import Register from './pages/Register'
import Pricing from './pages/Pricing'
import About from './pages/About'
import BottomNav from './components/BottomNav'
import './App.css'

function AnimatedRoutes() {
  const location = useLocation()
  
  return (
    <div className="page-transition-wrapper">
      <div key={location.pathname} className="page-transition">
        <Routes location={location}>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<Register />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </div>
  )
}

function App() {
  return (
    <RegistrationProvider>
      <Router>
        <div className="App">
          <AnimatedRoutes />
          <BottomNav />
        </div>
      </Router>
    </RegistrationProvider>
  )
}

export default App

