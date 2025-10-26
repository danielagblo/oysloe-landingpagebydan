import { useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'
import axios from 'axios'

// Generate or retrieve session ID
const getSessionId = () => {
  let sessionId = sessionStorage.getItem('analytics_session_id')
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    sessionStorage.setItem('analytics_session_id', sessionId)
  }
  return sessionId
}

export const useAnalytics = () => {
  const location = useLocation()
  const sessionId = useRef(getSessionId())
  const pageLoadTime = useRef(Date.now())
  const timeOnPage = useRef(0)
  const lastTrackedPath = useRef(null)

  // Track page view on route change
  useEffect(() => {
    const pagePath = location.pathname
    
    // Skip if we just tracked this path (avoid duplicates)
    if (lastTrackedPath.current === pagePath) {
      return
    }
    
    // Mark this path as tracked
    lastTrackedPath.current = pagePath
    
    // Reset time tracking for new page
    pageLoadTime.current = Date.now()
    timeOnPage.current = 0

    // Track page view with a small delay to ensure page is rendered
    const trackPageView = async () => {
      try {
        // Small delay to ensure page is fully loaded
        await new Promise(resolve => setTimeout(resolve, 200))
        
        const response = await axios.post('/api/analytics/track', {
          session_id: sessionId.current,
          page_path: pagePath,
          time_on_page: timeOnPage.current
        })
        
        if (response.data.success) {
          console.log('✅ Tracked page view:', pagePath)
        }
      } catch (error) {
        console.error('❌ Analytics tracking error for', pagePath, ':', error.message)
      }
    }

    // Track immediately
    trackPageView()

    // Track time on page every 10 seconds
    const interval = setInterval(() => {
      timeOnPage.current = Math.floor((Date.now() - pageLoadTime.current) / 1000)
    }, 10000)

    // Track session end when user leaves
    const handleBeforeUnload = () => {
      // Send session end event using sendBeacon
      const data = JSON.stringify({
        session_id: sessionId.current
      })
      const blob = new Blob([data], { type: 'application/json' })
      navigator.sendBeacon('/api/analytics/session-end', blob)
    }

    window.addEventListener('beforeunload', handleBeforeUnload)

    return () => {
      clearInterval(interval)
      window.removeEventListener('beforeunload', handleBeforeUnload)
      
      // Send final time on page
      const finalTimeOnPage = Math.floor((Date.now() - pageLoadTime.current) / 1000)
      if (finalTimeOnPage > 0) {
        // Update time on page via regular request (if available)
        try {
          axios.post('/api/analytics/track', {
            session_id: sessionId.current,
            page_path: pagePath,
            time_on_page: finalTimeOnPage
          }).catch(() => {
            // Ignore errors - this is cleanup
          })
        } catch (e) {
          // Ignore errors
        }
      }
    }
  }, [location.pathname])

  // Track session end on component unmount
  useEffect(() => {
    return () => {
      // Cleanup: track session end
      axios.post('/api/analytics/session-end', {
        session_id: sessionId.current
      }).catch(() => {
        // Ignore errors on cleanup
      })
    }
  }, [])
}

