import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './Pricing.css'

const Pricing = () => {
  const [plans, setPlans] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchPricingPlans = async () => {
      try {
        const response = await axios.get('/api/pricing')
        if (response.data.success) {
          setPlans(response.data.data)
        } else {
          setError('Failed to load pricing plans')
        }
      } catch (err) {
        console.error('Error fetching pricing plans:', err)
        setError('Failed to load pricing plans')
        // Fallback to default plans if API fails
        setPlans([
          {
            name: 'Basic',
            multiplier: '1.5x',
            features: [
              'Share limited number of ads',
              'All ads stays promoted for a week'
            ],
            currentPrice: '¢ 567',
            originalPrice: '¢ 567',
            badge: 'For you 50% off'
          },
          {
            name: 'Business',
            multiplier: '4x',
            features: [
              'Pro partnership status',
              'All ads stays promoted for a month'
            ],
            currentPrice: '¢ 567',
            originalPrice: '¢ 567'
          },
          {
            name: 'Platinum',
            multiplier: '10x',
            features: [
              'Unlimited number of ads',
              'Sell 10x faster in all categories'
            ],
            currentPrice: '¢ 567',
            originalPrice: '¢ 567'
          }
        ])
      } finally {
        setLoading(false)
      }
    }

    fetchPricingPlans()
  }, [])

  if (loading) {
    return (
      <div className="pricing-page">
        <div className="pricing-container">
          <div className="pricing-header">
            <p className="pricing-subtitle">Loading pricing plans...</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="pricing-page">
      <div className="pricing-container">
        <div className="pricing-header">
          <h1 className="pricing-title">We feature the simplest pricing module.</h1>
          <p className="pricing-subtitle">Pricing that works for all business types.</p>
        </div>

        {error && (
          <div style={{ color: '#ff6b6b', textAlign: 'center', marginBottom: '20px' }}>
            {error}
          </div>
        )}

        <div className="pricing-cards">
          {plans.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#888' }}>No pricing plans available</p>
          ) : (
            plans.map((plan, index) => (
              <div key={index} className="pricing-card">
                {plan.badge && (
                  <div className="pricing-badge">{plan.badge}</div>
                )}
                <div className="card-header">
                  <h2 className="plan-name">{plan.name}</h2>
                  <span className="plan-multiplier">{plan.multiplier}</span>
                </div>
                
                <div className="card-features">
                  {plan.features.map((feature, idx) => (
                    <div key={idx} className="feature-item">
                      <span className="checkmark">✓</span>
                      <span>{feature}</span>
                    </div>
                  ))}
                </div>

                <div className="card-pricing">
                  <span className="current-price">{plan.currentPrice}</span>
                  <span className="original-price">{plan.originalPrice}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

export default Pricing

