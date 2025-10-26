import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './AppScreenshotCarousel.css'

const AppScreenshotCarousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [screenshots, setScreenshots] = useState([])
  const [loading, setLoading] = useState(true)

  // Default fallback screenshots
  const defaultScreenshots = [
    { id: 1, name: 'Home Screen', color: '#E3F2FD' },
    { id: 2, name: 'Search Screen', color: '#F3E5F5' },
    { id: 3, name: 'Subscription Screen', color: '#E8F5E9' },
    { id: 4, name: 'Profile Screen', color: '#FFF3E0' },
    { id: 5, name: 'Category Screen', color: '#FCE4EC' }
  ]

  useEffect(() => {
    const fetchCarouselImages = async () => {
      try {
        const response = await axios.get('/api/carousel')
        if (response.data.success && response.data.data.length > 0) {
          setScreenshots(response.data.data)
        } else {
          // Use default screenshots if no images from API
          setScreenshots(defaultScreenshots)
        }
      } catch (err) {
        console.error('Error fetching carousel images:', err)
        // Use default screenshots on error
        setScreenshots(defaultScreenshots)
      } finally {
        setLoading(false)
      }
    }

    fetchCarouselImages()
  }, [])

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % screenshots.length)
  }

  const handlePrev = () => {
    setCurrentIndex((prev) => (prev - 1 + screenshots.length) % screenshots.length)
  }

  // Auto-scroll functionality
  useEffect(() => {
    if (screenshots.length === 0) return
    
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % screenshots.length)
    }, 5000) // Change slide every 5 seconds

    return () => clearInterval(interval)
  }, [screenshots.length])

  return (
    <div className="carousel-container">
      <div className="carousel-wrapper">
        <button className="carousel-btn carousel-btn-prev" onClick={handlePrev}>
          ‹
        </button>
        
        <div className="carousel-track">
          {screenshots.map((screenshot, index) => {
            const position = index - currentIndex
            const isActive = index === currentIndex
            
            return (
              <div
                key={screenshot.id}
                className={`carousel-slide ${isActive ? 'active' : ''}`}
                style={{
                  transform: `translateX(${position * 120}%) scale(${isActive ? 1 : 0.85})`,
                  opacity: isActive ? 1 : 0.6,
                  zIndex: isActive ? 2 : 1
                }}
              >
                <div className="screenshot-frame">
                  {screenshot.imageUrl ? (
                    <img 
                      src={screenshot.imageUrl} 
                      alt={screenshot.title}
                      className="screenshot-image"
                    />
                  ) : (
                    <div 
                      className="screenshot-placeholder"
                      style={{ backgroundColor: screenshot.color || '#E3F2FD' }}
                    >
                      <div className="screenshot-content">
                        <div className="screenshot-header">
                          <span className="status-bar">3:40</span>
                          <span className="app-title">Oysloe</span>
                        </div>
                        <div className="screenshot-body">
                          <div className="mock-search">🔍 Search anything...</div>
                          <div className="mock-grid">
                            {[...Array(6)].map((_, i) => (
                              <div key={i} className="mock-item"></div>
                            ))}
                          </div>
                        </div>
                        <div className="screenshot-footer">
                          <div className="nav-icon">🏠</div>
                          <div className="nav-icon">🔔</div>
                          <div className="nav-icon">➕</div>
                          <div className="nav-icon">📬</div>
                          <div className="nav-icon">👤</div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div className="screenshot-label">{screenshot.title || screenshot.name}</div>
                </div>
              </div>
            )
          })}
        </div>

        <button className="carousel-btn carousel-btn-next" onClick={handleNext}>
          ›
        </button>
      </div>

      {/* Carousel Indicators */}
      <div className="carousel-indicators">
        {screenshots.map((_, index) => (
          <button
            key={index}
            className={`indicator ${index === currentIndex ? 'active' : ''}`}
            onClick={() => setCurrentIndex(index)}
          />
        ))}
      </div>
    </div>
  )
}

export default AppScreenshotCarousel

