import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const RegistrationContext = createContext()

export const useRegistrationCount = () => {
  const context = useContext(RegistrationContext)
  if (!context) {
    throw new Error('useRegistrationCount must be used within RegistrationProvider')
  }
  return context
}

export const RegistrationProvider = ({ children }) => {
  const [count, setCount] = useState(0)
  const [loading, setLoading] = useState(true)

  const fetchCount = async () => {
    try {
      const response = await axios.get('/api/registrations/count')
      if (response.data.success) {
        setCount(response.data.count)
      }
    } catch (error) {
      console.error('Failed to fetch registration count:', error)
      // Keep the previous count on error
    } finally {
      setLoading(false)
    }
  }

  const refreshCount = async () => {
    await fetchCount()
  }

  useEffect(() => {
    fetchCount()
    // Poll every 30 seconds to keep count updated
    const interval = setInterval(fetchCount, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <RegistrationContext.Provider value={{ count, loading, refreshCount }}>
      {children}
    </RegistrationContext.Provider>
  )
}

