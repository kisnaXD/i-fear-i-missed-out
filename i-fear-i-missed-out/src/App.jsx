import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './Navbar/Navbar.jsx'; // Matches your structure
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import Calculators from './pages/Calculators';

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} /> 
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/calculators" element={<Calculators />} />
      </Routes>
    </div>
  );
}

export default App;