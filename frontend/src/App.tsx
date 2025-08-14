import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './pages/Dashboard'
import Traffic from './pages/Traffic'
import AirQuality from './pages/AirQuality'
import Energy from './pages/Energy'
import Emergency from './pages/Emergency'
import Analytics from './pages/Analytics'
import { useWebSocket } from './hooks/useWebSocket'
import { ThemeProvider } from './context/ThemeContext'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { data: realtimeData, isConnected } = useWebSocket('ws://localhost:8000/ws/realtime')

  return (
    <ThemeProvider>
      <Router>
        <div className="flex h-screen bg-gray-50 dark:bg-gray-900">
          {/* Sidebar */}
          <Sidebar isOpen={sidebarOpen} onToggle={setSidebarOpen} />
          
          {/* Main content */}
          <div className="flex-1 flex flex-col overflow-hidden">
            <Header 
              onMenuClick={() => setSidebarOpen(!sidebarOpen)}
              isConnected={isConnected}
            />
            
            <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 dark:bg-gray-900">
              <div className="container mx-auto px-6 py-8">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <Routes>
                    <Route path="/" element={<Dashboard realtimeData={realtimeData} />} />
                    <Route path="/traffic" element={<Traffic />} />
                    <Route path="/air-quality" element={<AirQuality />} />
                    <Route path="/energy" element={<Energy />} />
                    <Route path="/emergency" element={<Emergency />} />
                    <Route path="/analytics" element={<Analytics />} />
                  </Routes>
                </motion.div>
              </div>
            </main>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App