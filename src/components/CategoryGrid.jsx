import React from 'react'
import categoryImage from '../assets/category.png'
import './CategoryGrid.css'

const CategoryGrid = () => {
  return (
    <div className="category-grid-container">
      <img 
        src={categoryImage} 
        alt="Business Categories" 
        className="categories-image"
      />
    </div>
  )
}

export default CategoryGrid
