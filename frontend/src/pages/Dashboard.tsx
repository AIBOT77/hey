import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Car, 
  Wind, 
  Zap, 
  Users, 
  TrendingUp, 
  AlertTriangle,
  CheckCircle,
  Clock
} from 'lucide-react'
import MetricCard from '../components/MetricCard'
import Chart from '../components/Chart'
import Map from '../components/Map'
import axios from 'axios'

interface DashboardProps {
  realtimeData?: any
}

const Dashboard: React.FC<DashboardProps> = ({ realtimeData }) => {
  const [overview, setOverview] = useState<any>(null)
  const [cityHealth, setCityHealth] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, healthRes] = await Promise.all([
          axios.get('/api/dashboard/overview'),
          axios.get('/api/analytics/city-health')
        ])
        setOverview(overviewRes.data)
        setCityHealth(healthRes.data)
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const getStatusColor = (value: number, thresholds = { good: 0.8, warning: 0.6 }) => {
    if (value >= thresholds.good) return 'success'
    if (value >= thresholds.warning) return 'warning'
    return 'danger'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            City Overview
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Real-time insights powered by AI
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="status-indicator status-good"></div>
          <span className="text-sm text-gray-600 dark:text-gray-400">
            All systems operational
          </span>
        </div>
      </div>

      {/* City Health Score */}
      {cityHealth && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-6"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              City Health Score
            </h2>
            <div className="flex items-center space-x-2">
              <span className={`text-2xl font-bold ${
                cityHealth.grade === 'A' ? 'text-success-600' :
                cityHealth.grade === 'B' ? 'text-warning-600' : 'text-danger-600'
              }`}>
                {cityHealth.grade}
              </span>
              <span className="text-gray-500 dark:text-gray-400">
                ({(cityHealth.overall_score * 100).toFixed(0)}%)
              </span>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-4">
            {Object.entries(cityHealth.metrics).map(([key, value]: [string, any]) => (
              <div key={key} className="text-center">
                <div className="text-sm text-gray-600 dark:text-gray-400 capitalize mb-1">
                  {key.replace('_', ' ')}
                </div>
                <div className={`text-lg font-semibold ${
                  getStatusColor(value) === 'success' ? 'text-success-600' :
                  getStatusColor(value) === 'warning' ? 'text-warning-600' : 'text-danger-600'
                }`}>
                  {(value * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>

          {/* Recommendations */}
          <div>
            <h3 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
              AI Recommendations
            </h3>
            <ul className="space-y-1">
              {cityHealth.recommendations.map((rec: string, index: number) => (
                <li key={index} className="flex items-start space-x-2 text-sm text-gray-600 dark:text-gray-400">
                  <TrendingUp size={14} className="mt-0.5 text-primary-500 flex-shrink-0" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}

      {/* Metrics Grid */}
      {overview && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            title="Traffic Flow"
            value={`${(overview.traffic.congestion_level * 100).toFixed(0)}%`}
            subtitle="Congestion Level"
            icon={Car}
            trend={overview.traffic.congestion_level < 0.6 ? 'up' : 'down'}
            color={getStatusColor(1 - overview.traffic.congestion_level)}
          />
          
          <MetricCard
            title="Air Quality"
            value={overview.air_quality.aqi}
            subtitle="AQI Index"
            icon={Wind}
            trend={overview.air_quality.aqi < 100 ? 'up' : 'down'}
            color={getStatusColor(1 - overview.air_quality.aqi / 200)}
          />
          
          <MetricCard
            title="Energy Grid"
            value={`${overview.energy.grid_efficiency.toFixed(1)}%`}
            subtitle="Efficiency"
            icon={Zap}
            trend="up"
            color={getStatusColor(overview.energy.grid_efficiency / 100)}
          />
          
          <MetricCard
            title="Population"
            value={`${(overview.population.current_density * 100).toFixed(0)}%`}
            subtitle="Density"
            icon={Users}
            trend="stable"
            color="primary"
          />
        </div>
      )}

      {/* Charts and Map */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Real-time Chart */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Real-time Metrics
          </h3>
          <Chart data={realtimeData} />
        </motion.div>

        {/* City Map */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="card p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Live City Map
          </h3>
          <Map data={realtimeData} />
        </motion.div>
      </div>

      {/* Recent Alerts */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="card p-6"
      >
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Recent Alerts & Updates
        </h3>
        <div className="space-y-3">
          <div className="flex items-start space-x-3">
            <CheckCircle size={16} className="text-success-500 mt-0.5" />
            <div>
              <p className="text-sm text-gray-900 dark:text-white">
                Traffic optimization applied to downtown area
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">2 minutes ago</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <AlertTriangle size={16} className="text-warning-500 mt-0.5" />
            <div>
              <p className="text-sm text-gray-900 dark:text-white">
                Air quality sensor maintenance scheduled
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">15 minutes ago</p>
            </div>
          </div>
          <div className="flex items-start space-x-3">
            <Clock size={16} className="text-primary-500 mt-0.5" />
            <div>
              <p className="text-sm text-gray-900 dark:text-white">
                Energy consumption forecast updated
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">1 hour ago</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default Dashboard