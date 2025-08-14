import React from 'react'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts'

interface ChartProps {
  data?: any
  type?: 'line' | 'area'
  height?: number
}

const Chart: React.FC<ChartProps> = ({ data, type = 'area', height = 300 }) => {
  // Generate sample data if no real-time data available
  const sampleData = React.useMemo(() => {
    const now = new Date()
    return Array.from({ length: 24 }, (_, i) => {
      const time = new Date(now.getTime() - (23 - i) * 60 * 60 * 1000)
      return {
        time: time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        traffic: Math.random() * 100,
        airQuality: 50 + Math.random() * 50,
        energy: 70 + Math.random() * 30
      }
    })
  }, [])

  const chartData = data?.traffic ? [
    {
      time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
      traffic: data.traffic.live_count / 3, // Normalize to 0-100 scale
      airQuality: data.air_quality?.pm25 || 0,
      energy: data.energy?.current_load || 0
    }
  ] : sampleData

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white dark:bg-gray-800 p-3 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-900 dark:text-white">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toFixed(1)}
            </p>
          ))}
        </div>
      )
    }
    return null
  }

  if (type === 'line') {
    return (
      <ResponsiveContainer width="100%" height={height}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
          <XAxis 
            dataKey="time" 
            stroke="#6B7280"
            fontSize={12}
          />
          <YAxis 
            stroke="#6B7280"
            fontSize={12}
          />
          <Tooltip content={<CustomTooltip />} />
          <Line 
            type="monotone" 
            dataKey="traffic" 
            stroke="#3B82F6" 
            strokeWidth={2}
            name="Traffic"
            dot={{ r: 4 }}
          />
          <Line 
            type="monotone" 
            dataKey="airQuality" 
            stroke="#10B981" 
            strokeWidth={2}
            name="Air Quality"
            dot={{ r: 4 }}
          />
          <Line 
            type="monotone" 
            dataKey="energy" 
            stroke="#F59E0B" 
            strokeWidth={2}
            name="Energy"
            dot={{ r: 4 }}
          />
        </LineChart>
      </ResponsiveContainer>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
        <XAxis 
          dataKey="time" 
          stroke="#6B7280"
          fontSize={12}
        />
        <YAxis 
          stroke="#6B7280"
          fontSize={12}
        />
        <Tooltip content={<CustomTooltip />} />
        <Area
          type="monotone"
          dataKey="traffic"
          stackId="1"
          stroke="#3B82F6"
          fill="#3B82F6"
          fillOpacity={0.6}
          name="Traffic"
        />
        <Area
          type="monotone"
          dataKey="airQuality"
          stackId="2"
          stroke="#10B981"
          fill="#10B981"
          fillOpacity={0.6}
          name="Air Quality"
        />
        <Area
          type="monotone"
          dataKey="energy"
          stackId="3"
          stroke="#F59E0B"
          fill="#F59E0B"
          fillOpacity={0.6}
          name="Energy"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

export default Chart