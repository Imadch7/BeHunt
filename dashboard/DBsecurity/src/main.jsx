import { StrictMode } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { createRoot } from 'react-dom/client'
import Authenticate from './Authenticate.jsx';
import App from './App.jsx';
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/'element={<Authenticate />} />
        <Route path='/app' element={<App />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
