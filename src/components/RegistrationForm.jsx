import React, { useState } from 'react'
import axios from 'axios'
import { useRegistrationCount } from '../context/RegistrationContext'
import nameIcon from '../assets/name.png'
import emailIcon from '../assets/email.png'
import phoneIcon from '../assets/phone.png'
import businessNameIcon from '../assets/business name.png'
import businessCategoryIcon from '../assets/businesscategory.png'
import mapIcon from '../assets/map.png'
import './RegistrationForm.css'

const RegistrationForm = () => {
  const { refreshCount } = useRegistrationCount()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    businessName: '',
    businessCategory: '',
    location: ''
  })
  
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState(null)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    setSubmitStatus(null)

    try {
      const response = await axios.post('/api/register', formData)
      setSubmitStatus({ type: 'success', message: 'Registration successful!' })
      setFormData({
        name: '',
        email: '',
        phone: '',
        businessName: '',
        businessCategory: '',
        location: ''
      })
      // Refresh the registration count after successful registration
      await refreshCount()
    } catch (error) {
      setSubmitStatus({ 
        type: 'error', 
        message: error.response?.data?.message || 'Registration failed. Please try again.' 
      })
    } finally {
      setIsSubmitting(false)
    }
  }

  const categories = [
    'Electronics',
    'Furniture',
    'Vehicles',
    'Industry',
    'Grocery',
    'Games',
    'Cosmetics',
    'Property',
    'Fashion',
    'Services'
  ]

  return (
    <div className="registration-card">
      <h2 className="form-title">Register your business!</h2>
      <p className="registration-notice">Registration is ongoing</p>
      
      <form onSubmit={handleSubmit} className="registration-form">
        <div className="input-group">
          <img src={nameIcon} alt="Name" className="input-icon" />
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <img src={emailIcon} alt="Email" className="input-icon" />
          <input
            type="email"
            name="email"
            placeholder="Email Address"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <img src={phoneIcon} alt="Phone" className="input-icon" />
          <input
            type="tel"
            name="phone"
            placeholder="+233"
            value={formData.phone}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <img src={businessNameIcon} alt="Business Name" className="input-icon" />
          <input
            type="text"
            name="businessName"
            placeholder="Business name"
            value={formData.businessName}
            onChange={handleChange}
            required
          />
        </div>

        <div className="input-group">
          <img src={businessCategoryIcon} alt="Business Category" className="input-icon" />
          <select
            name="businessCategory"
            value={formData.businessCategory}
            onChange={handleChange}
            required
            className="select-input"
          >
            <option value="">Business category</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          <span className="select-arrow">▼</span>
        </div>

        <div className="input-group">
          <img src={mapIcon} alt="Location" className="input-icon" />
          <input
            type="text"
            name="location"
            placeholder="Location"
            value={formData.location}
            onChange={handleChange}
            required
          />
        </div>

        {submitStatus && (
          <div className={`submit-status ${submitStatus.type}`}>
            {submitStatus.message}
          </div>
        )}

        <button 
          type="submit" 
          className="register-button"
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Registering...' : 'Register'}
        </button>
      </form>

      <div className="benefits-list">
        <div className="benefit-item">
          <span className="checkmark">✓</span>
          <span>Improve your online presence and boost your business growth 10x.</span>
        </div>
        <div className="benefit-item">
          <span className="checkmark">✓</span>
          <span>Submit your business details via our form, to be registered.</span>
        </div>
        <div className="benefit-item">
          <span className="checkmark">✓</span>
          <span>Registering now secures up to six months free subscription.</span>
        </div>
      </div>
    </div>
  )
}

export default RegistrationForm

