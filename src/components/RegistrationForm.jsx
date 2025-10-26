import React, { useState, useEffect } from 'react'
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
  const [whatsappSettings, setWhatsappSettings] = useState({
    group_link: '',
    button_text: 'Join WhatsApp Group',
    is_active: false
  })

  useEffect(() => {
    const fetchWhatsAppSettings = async () => {
      try {
        const response = await axios.get('/api/whatsapp')
        if (response.data.success) {
          console.log('WhatsApp settings:', response.data.data)
          setWhatsappSettings(response.data.data)
        }
      } catch (error) {
        console.error('Error fetching WhatsApp settings:', error)
      }
    }

    fetchWhatsAppSettings()
  }, [])

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

      {whatsappSettings.is_active && (
        <div className="whatsapp-button-container">
          {whatsappSettings.group_link ? (
            <a
              href={whatsappSettings.group_link}
              target="_blank"
              rel="noopener noreferrer"
              className="whatsapp-join-button"
            >
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="whatsapp-icon"
              >
                <path
                  d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"
                  fill="currentColor"
                />
              </svg>
              {whatsappSettings.button_text}
            </a>
          ) : (
            <div className="whatsapp-join-button whatsapp-button-disabled">
              <svg
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="whatsapp-icon"
              >
                <path
                  d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"
                  fill="currentColor"
                />
              </svg>
              {whatsappSettings.button_text}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default RegistrationForm

