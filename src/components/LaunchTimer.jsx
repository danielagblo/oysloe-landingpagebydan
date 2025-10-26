import React, { useState, useEffect } from 'react'
import './LaunchTimer.css'

const LaunchTimer = () => {
  // Set launch date - adjust this to your actual launch date
  const launchDate = new Date('2025-12-25T23:59:59').getTime()

  const [timeLeft, setTimeLeft] = useState({
    days: 0,
    hours: 0,
    minutes: 0,
    seconds: 0
  })

  useEffect(() => {
    const calculateTimeLeft = () => {
      const now = new Date().getTime()
      const difference = launchDate - now

      if (difference > 0) {
        setTimeLeft({
          days: Math.floor(difference / (1000 * 60 * 60 * 24)),
          hours: Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
          minutes: Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60)),
          seconds: Math.floor((difference % (1000 * 60)) / 1000)
        })
      } else {
        setTimeLeft({ days: 0, hours: 0, minutes: 0, seconds: 0 })
      }
    }

    calculateTimeLeft()
    const interval = setInterval(calculateTimeLeft, 1000)

    return () => clearInterval(interval)
  }, [launchDate])

  return (
    <div className="launch-timer-container">
      <h2 className="timer-title">Launching Soon</h2>
      <p className="timer-subtitle">Get ready for an amazing experience</p>
      
      <div className="timer-grid">
        <div className="timer-unit">
          <div className="timer-value">{timeLeft.days}</div>
          <div className="timer-label">Days</div>
        </div>
        
        <div className="timer-separator">:</div>
        
        <div className="timer-unit">
          <div className="timer-value">{String(timeLeft.hours).padStart(2, '0')}</div>
          <div className="timer-label">Hours</div>
        </div>
        
        <div className="timer-separator">:</div>
        
        <div className="timer-unit">
          <div className="timer-value">{String(timeLeft.minutes).padStart(2, '0')}</div>
          <div className="timer-label">Minutes</div>
        </div>
        
        <div className="timer-separator">:</div>
        
        <div className="timer-unit">
          <div className="timer-value">{String(timeLeft.seconds).padStart(2, '0')}</div>
          <div className="timer-label">Seconds</div>
        </div>
      </div>
    </div>
  )
}

export default LaunchTimer

