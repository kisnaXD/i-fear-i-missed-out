import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { BrowserRouter } from 'react-router-dom';
import Navbar from './Navbar/Navbar.jsx';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import Calculators from './pages/Calculators';
import SPICalculator from './pages/SPICalculator';
import SWPCalculator from './pages/SWPCalculator';
import CompoundingCalculator from './pages/CompoundingCalculator';
import SimpleInterestCalculator from './pages/SimpleInterestCalculator';

function App() {
  console.log('App rendering, current path:', window.location.pathname);
  return (
    <div id="app-container">
      <Navbar />
      <div id="page-content">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/calculators" element={<Calculators />} />
            <Route path="/calculators/spi" element={<SPICalculator />} />
            <Route path="/calculators/swp" element={<SWPCalculator />} />
            <Route path="/calculators/compounding" element={<CompoundingCalculator />} />
            <Route path="/calculators/simple" element={<SimpleInterestCalculator />} />
          </Routes>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default App;