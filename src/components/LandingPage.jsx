import React, { useState, useEffect } from 'react'
import axios from 'axios'
import CategoryGrid from './CategoryGrid'
import RegistrationForm from './RegistrationForm'
import './LandingPage.css'

const LandingPage = () => {
  const [content, setContent] = useState({
    title: 'Sell anything safe<br />& fast on Oysloe.',
    subtitle: 'Improve your online presence and <strong>boost</strong> your business growth <strong class="text-10x">10x</strong>.'
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchLandingContent = async () => {
      try {
        const response = await axios.get('/api/landing')
        if (response.data.success) {
          setContent(response.data.data)
        }
      } catch (err) {
        console.error('Error fetching landing page content:', err)
        // Keep default content if API fails
      } finally {
        setLoading(false)
      }
    }

    fetchLandingContent()
  }, [])

  return (
    <div className="landing-page">
      <div className="landing-left">
        <div className="marketing-content">
          <h1 
            className="headline"
            dangerouslySetInnerHTML={{ __html: content.title }}
          />
          <p 
            className="sub-headline"
            dangerouslySetInnerHTML={{ __html: content.subtitle }}
          />
        </div>
        <CategoryGrid />
      </div>
      <div className="landing-right">
        <RegistrationForm />
      </div>
      <div className="landing-footer">
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
    </div>
  )
}

export default LandingPage

