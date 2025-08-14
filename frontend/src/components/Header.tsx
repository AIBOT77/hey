import React from 'react'
import { Menu, Sun, Moon, Wifi, WifiOff } from 'lucide-react'
import { useTheme } from '../context/ThemeContext'

interface HeaderProps {
  onMenuClick: () => void
  isConnected: boolean
}

const Header: React.FC<HeaderProps> = ({ onMenuClick, isConnected }) => {
  const { isDark, toggleTheme } = useTheme()

  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between px-6 py-4">
        <div className="flex items-center">
          <button
            onClick={onMenuClick}
            className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 lg:hidden"
          >
            <Menu size={24} />
          </button>
          <h1 className="ml-4 text-2xl font-bold text-gray-900 dark:text-white">
            Smart City Dashboard
          </h1>
        </div>

        <div className="flex items-center space-x-4">
          {/* Connection Status */}
          <div className="flex items-center space-x-2">
            {isConnected ? (
              <>
                <Wifi size={16} className="text-success-500" />
                <span className="text-sm text-success-600 dark:text-success-400">Live</span>
              </>
            ) : (
              <>
                <WifiOff size={16} className="text-danger-500" />
                <span className="text-sm text-danger-600 dark:text-danger-400">Offline</span>
              </>
            )}
          </div>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            {isDark ? <Sun size={18} /> : <Moon size={18} />}
          </button>

          {/* User Avatar */}
          <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center">
            <span className="text-white text-sm font-medium">AI</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header