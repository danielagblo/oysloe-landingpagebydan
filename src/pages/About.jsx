import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { useRegistrationCount } from '../context/RegistrationContext'
import AppScreenshotCarousel from '../components/AppScreenshotCarousel'
import LaunchTimer from '../components/LaunchTimer'
import './About.css'

const About = () => {
  const { count, loading: countLoading } = useRegistrationCount()
  const [aboutData, setAboutData] = useState({
    title: 'About Oysloe',
    description: 'Oysloe is your trusted marketplace for buying and selling safely and quickly. We provide a platform that connects buyers and sellers across various categories, making commerce simple and efficient.',
    satisfactionRate: '95%',
    features: [
      { icon: '🛡️', title: 'Safe Transactions', text: 'We prioritize your security with verified sellers and secure payment options.' },
      { icon: '⚡', title: 'Fast & Easy', text: 'Post your ads in minutes and connect with buyers instantly.' },
      { icon: '📱', title: 'Multiple Categories', text: 'From electronics to real estate, find or sell anything you need.' },
      { icon: '🚀', title: 'Boost Your Business', text: 'Reach more customers and grow your business with our promotion tools.' }
    ],
    contactInfo: [
      { location: 'Accra, Ghana', phone: '+233 XX XXX XXXX', email: 'info@oysloe.com' }
    ]
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAboutContent = async () => {
      try {
        const response = await axios.get('/api/about')
        if (response.data.success) {
          setAboutData(response.data.data)
        }
      } catch (err) {
        console.error('Error fetching about content:', err)
        // Keep default data if API fails
      } finally {
        setLoading(false)
      }
    }

    fetchAboutContent()
  }, [])

  const formatCount = (num) => {
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K+`
    }
    return `${num}+`
  }

  // Each registered user counts as 10 waiting listings
  const waitingListings = count * 10

  return (
    <div className="about-page">
      <div className="about-container">
        {/* Hero Section with App Screenshot Carousel */}
        <section className="about-hero">
          <AppScreenshotCarousel />
        </section>

        {/* Launch Timer Section */}
        <LaunchTimer />

        {/* About Content Section */}
        <section className="about-content">
          <h1 className="about-title">{aboutData.title}</h1>
          <p className="about-description">
            {aboutData.description}
          </p>

          <div className="about-features">
            {aboutData.features.map((feature, index) => (
              <div key={index} className="feature-card">
                <div className="feature-icon">{feature.icon}</div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-text">{feature.text}</p>
              </div>
            ))}
          </div>

          <div className="about-stats">
            <div className="stat-item">
              <div className="stat-number">
                {countLoading ? '...' : formatCount(count)}
              </div>
              <div className="stat-label">Users Waiting</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">
                {countLoading ? '...' : formatCount(waitingListings)}
              </div>
              <div className="stat-label">Waiting Listings</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">{aboutData.satisfactionRate}</div>
              <div className="stat-label">Satisfaction Rate</div>
            </div>
          </div>

          {/* Contact Information Section */}
          {aboutData.contactInfo && aboutData.contactInfo.length > 0 && (
            <div className="contact-section">
              <h2 className="contact-title">Contact Us</h2>
              <div className="contact-info">
                {aboutData.contactInfo.map((contact, index) => (
                  <React.Fragment key={index}>
                    <div className="contact-item">
                      <div className="contact-icon">📍</div>
                      <div className="contact-details">
                        <div className="contact-label">Location</div>
                        <div className="contact-value">{contact.location}</div>
                      </div>
                    </div>
                    {contact.phone && (
                      <div className="contact-item">
                        <div className="contact-icon">📞</div>
                        <div className="contact-details">
                          <div className="contact-label">Phone</div>
                          <div className="contact-value">{contact.phone}</div>
                        </div>
                      </div>
                    )}
                    {contact.email && (
                      <div className="contact-item">
                        <div className="contact-icon">✉️</div>
                        <div className="contact-details">
                          <div className="contact-label">Email</div>
                          <div className="contact-value">{contact.email}</div>
                        </div>
                      </div>
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>
          )}

          {/* Footer Section */}
          <div className="about-footer">
            <p className="footer-text">
              Designed & Owned by{' '}
              <a 
                href="https://bricsky.com" 
                target="_blank" 
                rel="noopener noreferrer"
                className="footer-link"
              >
                Bricsky Software
              </a>
            </p>
          </div>
        </section>
      </div>
    </div>
  )
}

export default About

