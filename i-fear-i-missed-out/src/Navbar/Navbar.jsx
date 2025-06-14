import React, { useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const [blobPosition, setBlobPosition] = useState({ x: 0, y: 0 });
  const [isHovering, setIsHovering] = useState(false);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const elementsRef = useRef(null);

  const handleMouseMove = (e) => {
    if (!elementsRef.current) return;
    const rect = elementsRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const blobSize = 50;
    const clampedX = Math.max(blobSize / 2, Math.min(x, rect.width - blobSize / 2));
    const clampedY = Math.max(blobSize / 2, Math.min(y, rect.height - blobSize / 2));
    setBlobPosition({ x: clampedX, y: clampedY });
    console.log(`Mouse move: x=${clampedX}, y=${clampedY}, navbar-elements: width=${rect.width}, height=${rect.height}`);
  };

  const handleMouseEnter = () => {
    setIsHovering(true);
    console.log('Mouse entered navbar-elements');
  };

  const handleMouseLeave = () => {
    setIsHovering(false);
    console.log('Mouse left navbar-elements');
  };

  const handleDropdownToggle = (e) => {
    setIsDropdownOpen((prev) => !prev);
    e.stopPropagation(); // Prevent blob movement on click
  };

  return (
    <div className="navbar-container">
      <div className="navbar-logo">
        Missed <br /> Out?
      </div>
      <div
        className="navbar-elements"
        ref={elementsRef}
        onMouseMove={handleMouseMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <Link to="/">Home</Link>
        <Link to="/about">About Us</Link>
        <Link to="/contact">Contact Us</Link>
        <div className="dropdown" onClick={handleDropdownToggle}>
          <Link to="/calculators" className="nav-link dropdown-toggle">
            Other Calculators
          </Link>
          {isDropdownOpen && (
            <div className="dropdown-menu">
              <Link to="/calculators/spi">SPI Calculator</Link>
              <Link to="/calculators/swp">SWP Calculator</Link>
              <Link to="/calculators/compounding">Compounding Calculator</Link>
              <Link to="/calculators/simple">Simple Interest Calculator</Link>
            </div>
          )}
        </div>
        {isHovering && (
          <div
            className="navbar-blob"
            style={{
              left: `${blobPosition.x - 25}px`,
              top: `${blobPosition.y - 25}px`,
            }}
          />
        )}
      </div>
    </div>
  );
};

export default Navbar;