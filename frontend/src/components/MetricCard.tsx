import React from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, Minus, LucideIcon } from 'lucide-react'

interface MetricCardProps {
  title: string
  value: string | number
  subtitle?: string
  icon: LucideIcon
  trend?: 'up' | 'down' | 'stable'
  color?: 'primary' | 'success' | 'warning' | 'danger'
  loading?: boolean
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  color = 'primary',
  loading = false
}) => {
  const colorClasses = {
    primary: 'bg-primary-100 text-primary-600 dark:bg-primary-900 dark:text-primary-400',
    success: 'bg-success-100 text-success-600 dark:bg-success-900 dark:text-success-400',
    warning: 'bg-warning-100 text-warning-600 dark:bg-warning-900 dark:text-warning-400',
    danger: 'bg-danger-100 text-danger-600 dark:bg-danger-900 dark:text-danger-400'
  }

  const trendIcons = {
    up: TrendingUp,
    down: TrendingDown,
    stable: Minus
  }

  const trendColors = {
    up: 'text-success-500',
    down: 'text-danger-500',
    stable: 'text-gray-500'
  }

  const TrendIcon = trend ? trendIcons[trend] : null

  if (loading) {
    return (
      <div className="metric-card">
        <div className="animate-pulse">
          <div className="flex items-center justify-between mb-4">
            <div className="w-8 h-8 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
            <div className="w-4 h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
          <div className="space-y-2">
            <div className="w-16 h-8 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="w-24 h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
            <div className="w-20 h-3 bg-gray-200 dark:bg-gray-700 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <motion.div
      whileHover={{ y: -2 }}
      transition={{ type: 'spring', stiffness: 300 }}
      className="metric-card"
    >
      <div className="flex items-center justify-between mb-4">
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
          <Icon size={20} />
        </div>
        {TrendIcon && (
          <TrendIcon size={16} className={trendColors[trend!]} />
        )}
      </div>
      
      <div className="space-y-1">
        <div className="text-2xl font-bold text-gray-900 dark:text-white">
          {value}
        </div>
        {subtitle && (
          <div className="text-sm text-gray-600 dark:text-gray-400">
            {subtitle}
          </div>
        )}
        <div className="text-xs font-medium text-gray-500 dark:text-gray-500 uppercase tracking-wide">
          {title}
        </div>
      </div>
    </motion.div>
  )
}

export default MetricCard