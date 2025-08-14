import React from 'react'

interface MapProps {
  data?: any
  height?: number
}

const Map: React.FC<MapProps> = ({ data, height = 300 }) => {
  // For demo purposes, create a simple SVG-based map visualization
  // In a real implementation, you'd use react-leaflet or similar
  
  const generatePoints = () => {
    if (data?.traffic?.congestion_points) {
      return data.traffic.congestion_points.map((point: any, index: number) => ({
        id: index,
        x: ((point.lng + 74.0060) * 1000) % 100,
        y: ((point.lat - 40.7128) * 1000) % 100,
        severity: point.severity,
        type: 'traffic'
      }))
    }
    
    // Generate sample points
    return Array.from({ length: 8 }, (_, i) => ({
      id: i,
      x: Math.random() * 80 + 10,
      y: Math.random() * 60 + 20,
      severity: Math.random(),
      type: Math.random() > 0.5 ? 'traffic' : 'air'
    }))
  }

  const points = generatePoints()

  const getPointColor = (type: string, severity: number) => {
    if (type === 'traffic') {
      if (severity > 0.7) return '#EF4444' // Red
      if (severity > 0.4) return '#F59E0B' // Yellow
      return '#10B981' // Green
    } else {
      if (severity > 0.7) return '#8B5CF6' // Purple
      if (severity > 0.4) return '#3B82F6' // Blue
      return '#06B6D4' // Cyan
    }
  }

  return (
    <div className="relative bg-gray-100 dark:bg-gray-700 rounded-lg overflow-hidden" style={{ height }}>
      {/* Grid background */}
      <svg className="absolute inset-0 w-full h-full">
        <defs>
          <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
            <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#D1D5DB" strokeWidth="0.5" opacity="0.3"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
        
        {/* City blocks (simplified) */}
        <rect x="20%" y="30%" width="15%" height="20%" fill="#E5E7EB" rx="2" />
        <rect x="40%" y="25%" width="20%" height="25%" fill="#E5E7EB" rx="2" />
        <rect x="65%" y="35%" width="18%" height="15%" fill="#E5E7EB" rx="2" />
        <rect x="25%" y="55%" width="25%" height="20%" fill="#E5E7EB" rx="2" />
        <rect x="55%" y="60%" width="20%" height="18%" fill="#E5E7EB" rx="2" />
        
        {/* Roads */}
        <line x1="0%" y1="45%" x2="100%" y2="45%" stroke="#9CA3AF" strokeWidth="3" />
        <line x1="35%" y1="0%" x2="35%" y2="100%" stroke="#9CA3AF" strokeWidth="3" />
        <line x1="60%" y1="0%" x2="60%" y2="100%" stroke="#9CA3AF" strokeWidth="2" />
        
        {/* Data points */}
        {points.map((point) => (
          <g key={point.id}>
            <circle
              cx={`${point.x}%`}
              cy={`${point.y}%`}
              r="6"
              fill={getPointColor(point.type, point.severity)}
              opacity="0.8"
              className="animate-pulse"
            />
            <circle
              cx={`${point.x}%`}
              cy={`${point.y}%`}
              r="12"
              fill={getPointColor(point.type, point.severity)}
              opacity="0.2"
              className="animate-ping"
            />
          </g>
        ))}
      </svg>
      
      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-white dark:bg-gray-800 rounded-lg p-3 shadow-lg">
        <div className="text-xs font-medium text-gray-900 dark:text-white mb-2">Live Data</div>
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-xs text-gray-600 dark:text-gray-400">High Traffic</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-xs text-gray-600 dark:text-gray-400">Medium Traffic</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-xs text-gray-600 dark:text-gray-400">Low Traffic</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-purple-500"></div>
            <span className="text-xs text-gray-600 dark:text-gray-400">Air Quality</span>
          </div>
        </div>
      </div>
      
      {/* Real-time indicator */}
      <div className="absolute top-4 right-4 flex items-center space-x-2 bg-white dark:bg-gray-800 rounded-lg px-3 py-1 shadow-lg">
        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
        <span className="text-xs text-gray-600 dark:text-gray-400">Live Updates</span>
      </div>
    </div>
  )
}

export default Map