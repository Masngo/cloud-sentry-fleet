import React, { useState } from 'react';
import { 
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, 
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';
import { LayoutDashboard, BarChart2, Settings, ChevronLeft, ChevronRight, Filter } from 'lucide-react';

const mockActivityData = [
  { name: 'Mon', active: 400, resolved: 240 },
  { name: 'Tue', active: 300, resolved: 139 },
  { name: 'Wed', active: 520, resolved: 980 },
  { name: 'Thu', active: 278, resolved: 390 },
  { name: 'Fri', active: 189, resolved: 480 },
];

const mockPieData = [
  { name: 'Low', value: 400, color: '#10B981' },
  { name: 'Medium', value: 300, color: '#F59E0B' },
  { name: 'High', value: 300, color: '#EF4444' },
];

export default function AdvancedDashboard() {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState('7d');

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans">
      <aside className={`${collapsed ? 'w-20' : 'w-64'} transition-all duration-300 bg-slate-900 border-r border-slate-800 flex flex-col justify-between p-4`}>
        <div>
          <div className="flex items-center justify-between mb-8">
            {!collapsed && <span className="font-bold text-lg text-blue-400">ControlPanel</span>}
            <button 
              onClick={() => setCollapsed(!collapsed)} 
              className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300"
            >
              {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
            </button>
          </div>

          <nav className="space-y-2">
            <a href="#" className="flex items-center space-x-3 p-3 rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30">
              <LayoutDashboard size={20} />
              {!collapsed && <span className="font-medium">Overview</span>}
            </a>
            <a href="#" className="flex items-center space-x-3 p-3 rounded-xl text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors">
              <BarChart2 size={20} />
              {!collapsed && <span className="font-medium">Analytics</span>}
            </a>
            <a href="#" className="flex items-center space-x-3 p-3 rounded-xl text-slate-400 hover:bg-slate-800 hover:text-slate-200 transition-colors">
              <Settings size={20} />
              {!collapsed && <span className="font-medium">Settings</span>}
            </a>
          </nav>
        </div>

        {!collapsed && (
          <div className="p-3 bg-slate-800/50 rounded-xl border border-slate-800">
            <div className="flex items-center space-x-2 text-xs text-slate-400 mb-2">
              <Filter size={14} />
              <span>Timeframe</span>
            </div>
            <select 
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg p-1.5 text-sm focus:outline-none focus:border-blue-500 text-slate-200"
            >
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
            </select>
          </div>
        )}
      </aside>

      <main className="flex-1 overflow-y-auto p-8 space-y-6">
        <div className="flex justify-between items-center border-b border-slate-800 pb-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">System Telemetry</h1>
            <p className="text-sm text-slate-400">Real-time metrics and system analytical distribution</p>
          </div>
          <button className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded-lg font-medium text-sm transition-colors shadow-lg shadow-blue-500/20">
            Export Report
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
            <h2 className="text-base font-semibold mb-4 text-slate-200">Execution Activity Trend</h2>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockActivityData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" stroke="#94A3B8" />
                  <YAxis stroke="#94A3B8" />
                  <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }} />
                  <Line type="monotone" dataKey="active" stroke="#3B82F6" strokeWidth={3} dot={{ r: 4 }} />
                  <Line type="monotone" dataKey="resolved" stroke="#10B981" strokeWidth={3} dot={{ r: 4 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl flex flex-col justify-between">
            <h2 className="text-base font-semibold mb-2 text-slate-200">Severity Distribution</h2>
            <div className="h-60">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={mockPieData} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={5}>
                    {mockPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex justify-around text-xs text-slate-400 border-t border-slate-800 pt-3">
              {mockPieData.map((item) => (
                <div key={item.name} className="flex items-center space-x-1">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                  <span>{item.name}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
          <h2 className="text-base font-semibold mb-4 text-slate-200">Volume Output Comparison</h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockActivityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="name" stroke="#94A3B8" />
                <YAxis stroke="#94A3B8" />
                <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px' }} />
                <Bar dataKey="active" fill="#6366F1" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </main>
    </div>
  );
}
