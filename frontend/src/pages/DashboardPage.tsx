import React, { useState, useEffect } from 'react';
import type { DashboardStats, AIInsightItem } from '../types';
import { fetchAIInsights } from '../api';
import { Users, Flame, PhoneCall, Calendar, ArrowUpRight, Globe, Clock, ChevronRight, Bot, Sparkles } from 'lucide-react';
import { StatusDot } from '../components/StatusDot';

interface DashboardPageProps {
  stats: DashboardStats | null;
  loading: boolean;
  onSelectLead: (leadId: number) => void;
  setActiveTab: (tab: string) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({
  stats,
  loading,
  onSelectLead,
  setActiveTab,
}) => {
  const [aiInsights, setAiInsights] = useState<AIInsightItem[]>([]);
  const [insightsLoading, setInsightsLoading] = useState(true);

  useEffect(() => {
    fetchAIInsights()
      .then((data) => setAiInsights(data.insights))
      .catch((err) => console.error('Failed to fetch AI insights:', err))
      .finally(() => setInsightsLoading(false));
  }, []);

  if (loading || !stats) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  const hotPercentage = stats.total_leads > 0 
    ? Math.round((stats.hot_leads_count / stats.total_leads) * 100) 
    : 0;

  const statCards = [
    {
      title: 'Total Leads',
      value: stats.total_leads,
      icon: Users,
      color: 'text-purple-600',
      bg: 'bg-purple-50',
      trend: '+12% this week',
    },
    {
      title: 'Hot Leads',
      value: stats.hot_leads_count,
      icon: Flame,
      color: 'text-red-600',
      bg: 'bg-red-50',
      trend: 'High Intent',
    },
    {
      title: 'Calls Today',
      value: stats.calls_today_count,
      icon: PhoneCall,
      color: 'text-indigo-600',
      bg: 'bg-indigo-50',
      trend: '24/7 AI Active',
    },
    {
      title: 'Pending Follow-Ups',
      value: stats.pending_follow_ups_count,
      icon: Calendar,
      color: 'text-amber-600',
      bg: 'bg-amber-50',
      trend: 'Action Required',
    },
  ];

  return (
    <div className="space-y-8 pb-12">
      {/* Hero Banner / Value Proposition */}
      <div className="bg-gradient-to-r from-purple-900 via-indigo-900 to-gray-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 translate-x-12 -translate-y-12 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 max-w-2xl">
          <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-purple-500/20 text-purple-200 border border-purple-400/30 mb-4">
            Autonomous Bilingual Voice Sales Agent
          </span>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white mb-2">
            Turning Voice Conversations into Qualified CRM Pipeline
          </h1>
          <p className="text-gray-300 text-sm sm:text-base leading-relaxed mb-6">
            LinguaLead automatically answers inbound calls in Urdu or English, extracts buyer intent, scores leads, and schedules follow-ups.
          </p>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => setActiveTab('leads')}
              className="px-5 py-2.5 rounded-xl bg-white text-gray-900 font-semibold text-sm hover:bg-gray-100 transition shadow-md flex items-center space-x-2"
            >
              <span>View All Leads</span>
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => setActiveTab('demo')}
              className="px-5 py-2.5 rounded-xl bg-purple-600 text-white font-semibold text-sm hover:bg-purple-500 transition shadow-md shadow-purple-900/40 flex items-center space-x-2"
            >
              <span>Test AI Call Demo</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Grid: Left content + Right AI Assistant Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left 2 Columns: Stats, Progress Ring, Recent Leads, Recent Calls */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Stats Grid + Conversion Ring */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            {statCards.map((card, idx) => {
              const Icon = card.icon;
              return (
                <div
                  key={idx}
                  className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100 hover:shadow-md transition-all duration-200 flex flex-col justify-between"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div className={`w-12 h-12 rounded-2xl ${card.bg} ${card.color} flex items-center justify-center`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-gray-50 text-gray-600 border border-gray-100">
                      {card.trend}
                    </span>
                  </div>
                  <div>
                    <h3 className="text-gray-500 text-sm font-medium">{card.title}</h3>
                    <p className="text-3xl font-bold text-gray-900 mt-1">{card.value}</p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Hot Lead Conversion Rate Ring Card (Inspired by design reference) */}
          <div className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100 flex flex-col sm:flex-row items-center justify-between gap-6">
            <div className="space-y-2 text-center sm:text-left">
              <span className="text-xs font-bold uppercase tracking-wider text-purple-600 bg-purple-50 px-3 py-1 rounded-full border border-purple-100">
                Pipeline Quality
              </span>
              <h3 className="text-lg font-bold text-gray-900">High-Intent Hot Lead Ratio</h3>
              <p className="text-xs text-gray-500 max-w-md">
                Percentage of captured prospects qualified as high-intent hot buyers requiring immediate closing attention.
              </p>
            </div>
            <div className="flex items-center space-x-6">
              <div className="relative w-24 h-24 flex items-center justify-center">
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    className="text-gray-100"
                    strokeWidth="3.5"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className="text-purple-600"
                    strokeDasharray={`${hotPercentage}, 100`}
                    strokeWidth="3.5"
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <div className="absolute text-sm font-bold text-gray-900">{hotPercentage}%</div>
              </div>
              <div className="space-y-1 text-right sm:text-left">
                <div className="text-2xl font-bold text-gray-900">{stats.hot_leads_count} / {stats.total_leads}</div>
                <div className="text-xs text-gray-400">Qualified Hot Leads</div>
              </div>
            </div>
          </div>

          {/* Recent Leads Table */}
          <div className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-gray-900">Recent Leads</h2>
                <p className="text-xs text-gray-500">Latest prospects captured by the AI agent</p>
              </div>
              <button
                onClick={() => setActiveTab('leads')}
                className="text-sm font-semibold text-purple-600 hover:text-purple-700 flex items-center space-x-1"
              >
                <span>See all</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-gray-100 text-xs font-semibold text-gray-400 uppercase tracking-wider">
                    <th className="pb-3 px-3">Lead Name</th>
                    <th className="pb-3 px-3">Status</th>
                    <th className="pb-3 px-3">Language</th>
                    <th className="pb-3 px-3">Phone</th>
                    <th className="pb-3 px-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-50 text-sm">
                  {stats.recent_leads.map((lead) => (
                    <tr key={lead.id} className="hover:bg-gray-50/80 transition cursor-pointer" onClick={() => onSelectLead(lead.id)}>
                      <td className="py-4 px-3 font-semibold text-gray-900 flex items-center space-x-3">
                        <div className="w-9 h-9 rounded-full bg-purple-100 text-purple-700 font-bold flex items-center justify-center text-xs">
                          {lead.name.charAt(0)}
                        </div>
                        <div>
                          <div>{lead.name}</div>
                          <div className="text-xs text-gray-400 font-normal">{lead.total_calls} call(s)</div>
                        </div>
                      </td>
                      <td className="py-4 px-3">
                        <StatusDot status={lead.latest_qualification || lead.status} />
                      </td>
                      <td className="py-4 px-3 capitalize text-gray-600 flex items-center space-x-1.5 pt-5">
                        <Globe className="w-3.5 h-3.5 text-gray-400" />
                        <span>{lead.language}</span>
                      </td>
                      <td className="py-4 px-3 text-gray-600 font-mono text-xs">{lead.phone}</td>
                      <td className="py-4 px-3 text-right">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            onSelectLead(lead.id);
                          }}
                          className="p-2 rounded-xl text-gray-400 hover:text-purple-600 hover:bg-purple-50 transition"
                        >
                          <ChevronRight className="w-4 h-4" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Recent Calls Feed */}
          <div className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-gray-900">Recent Calls</h2>
                <p className="text-xs text-gray-500">Live call summaries</p>
              </div>
              <PhoneCall className="w-5 h-5 text-purple-600" />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {stats.recent_calls.map((call) => (
                <div key={call.id} className="p-4 rounded-2xl bg-gray-50/80 border border-gray-100 space-y-2">
                  <div className="flex items-center justify-between">
                    <StatusDot status={call.qualification_score || 'warm'} />
                    <span className="text-xs text-gray-400 flex items-center space-x-1">
                      <Clock className="w-3 h-3" />
                      <span>{call.duration_seconds}s</span>
                    </span>
                  </div>
                  <p className="text-xs text-gray-700 line-clamp-2 font-medium">
                    {call.summary || call.transcript || 'Call completed.'}
                  </p>
                  <div className="text-[11px] text-gray-400 font-mono">
                    {new Date(call.created_at).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Right Column: AI Assistant Feed Panel (Inspired by design reference) */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100 flex flex-col h-full sticky top-6">
            <div className="flex items-center justify-between mb-5">
              <div className="flex items-center space-x-2.5">
                <div className="w-9 h-9 rounded-2xl bg-purple-100 text-purple-700 flex items-center justify-center shadow-inner">
                  <Bot className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-gray-900">AI Assistant</h2>
                  <p className="text-[11px] text-gray-400">Autonomous CRM Analyst</p>
                </div>
              </div>
              <span className="inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-semibold bg-purple-50 text-purple-700 border border-purple-100">
                <Sparkles className="w-3 h-3 mr-1 text-purple-500" /> Live
              </span>
            </div>

            <div className="space-y-4 flex-1 overflow-y-auto max-h-[700px] pr-1">
              {insightsLoading ? (
                <div className="flex justify-center py-12">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-purple-600"></div>
                </div>
              ) : aiInsights.length === 0 ? (
                <div className="text-center py-12 px-4 bg-purple-50/30 rounded-2xl border border-purple-100/50 space-y-2">
                  <div className="w-10 h-10 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center mx-auto">
                    ✨
                  </div>
                  <p className="text-xs text-gray-600 font-semibold">All Caught Up!</p>
                  <p className="text-[11px] text-gray-400">No urgent items or overdue follow-ups right now.</p>
                </div>
              ) : (
                aiInsights.map((insight) => (
                  <div
                    key={insight.id}
                    className="p-4 rounded-2xl bg-gradient-to-br from-purple-50/60 to-indigo-50/30 border border-purple-100/70 space-y-2 shadow-xs"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-purple-900 flex items-center">
                        <span className="w-2 h-2 rounded-full bg-purple-500 mr-1.5 animate-pulse" />
                        {insight.title}
                      </span>
                      <span className="text-[10px] text-gray-400 font-mono">
                        {new Date(insight.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                    <p className="text-xs text-gray-700 leading-relaxed font-medium">
                      {insight.message}
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
