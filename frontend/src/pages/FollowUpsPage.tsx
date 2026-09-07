import React, { useState, useEffect } from 'react';
import type { FollowUp } from '../types';
import { fetchFollowUps, updateFollowUp } from '../api';
import { Calendar, CheckCircle2, Clock, Phone, User, Filter } from 'lucide-react';

interface FollowUpsPageProps {
  onSelectLead: (leadId: number) => void;
}

export const FollowUpsPage: React.FC<FollowUpsPageProps> = ({ onSelectLead }) => {
  const [followUps, setFollowUps] = useState<FollowUp[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterCompleted, setFilterCompleted] = useState<string>('false');

  useEffect(() => {
    loadFollowUps();
  }, [filterCompleted]);

  const loadFollowUps = async () => {
    try {
      setLoading(true);
      const completedParam = filterCompleted === 'all' ? undefined : filterCompleted === 'true';
      const data = await fetchFollowUps(completedParam);
      setFollowUps(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleComplete = async (id: number, currentCompleted: boolean) => {
    try {
      await updateFollowUp(id, !currentCompleted);
      loadFollowUps();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header & Filter */}
      <div className="bg-white rounded-2xl p-6 shadow-xs border border-gray-100 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Follow-Up Action Queue</h1>
          <p className="text-sm text-gray-500">Automated 24-hour follow-up tasks for hot & warm leads</p>
        </div>
        <div className="flex items-center space-x-3">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={filterCompleted}
            onChange={(e) => setFilterCompleted(e.target.value)}
            className="px-4 py-2.5 rounded-xl border border-gray-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500"
          >
            <option value="false">Pending Only</option>
            <option value="true">Completed Only</option>
            <option value="all">All Follow-Ups</option>
          </select>
        </div>
      </div>

      {/* Follow-Ups List */}
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-purple-600 border-t-transparent"></div>
        </div>
      ) : followUps.length === 0 ? (
        <div className="bg-white rounded-2xl p-12 text-center border border-gray-100">
          <Calendar className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-gray-800">No follow-ups found</h3>
          <p className="text-sm text-gray-500 mt-1">All caught up on client follow-up actions!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {followUps.map((fu) => (
            <div
              key={fu.id}
              className={`bg-white rounded-2xl p-6 shadow-xs border transition space-y-4 ${
                fu.completed ? 'border-gray-100 opacity-70 bg-gray-50/50' : 'border-purple-100 hover:shadow-md'
              }`}
            >
              <div className="flex items-start justify-between">
                <div
                  className="cursor-pointer group"
                  onClick={() => onSelectLead(fu.lead_id)}
                >
                  <h3 className="font-bold text-gray-900 group-hover:text-purple-600 transition flex items-center">
                    <User className="w-4 h-4 mr-1.5 text-purple-600" />
                    {fu.lead_name || 'Valued Lead'}
                  </h3>
                  <p className="text-xs text-gray-500 font-mono mt-0.5 flex items-center">
                    <Phone className="w-3 h-3 mr-1 text-gray-400" />
                    {fu.lead_phone || 'N/A'}
                  </p>
                </div>
                <button
                  onClick={() => handleToggleComplete(fu.id, fu.completed)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center space-x-1.5 transition shadow-xs ${
                    fu.completed
                      ? 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                      : 'bg-purple-600 text-white hover:bg-purple-500 shadow-purple-500/20'
                  }`}
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>{fu.completed ? 'Completed' : 'Mark Done'}</span>
                </button>
              </div>

              <div className="p-3.5 rounded-xl bg-gray-50 border border-gray-100 text-xs text-gray-700 font-medium">
                {fu.notes || 'Scheduled follow-up action.'}
              </div>

              <div className="flex items-center justify-between text-xs text-gray-400 pt-2 border-t border-gray-50">
                <span className="flex items-center">
                  <Clock className="w-3.5 h-3.5 mr-1 text-gray-400" />
                  Scheduled: {new Date(fu.scheduled_for).toLocaleString()}
                </span>
                <button
                  onClick={() => onSelectLead(fu.lead_id)}
                  className="text-purple-600 font-semibold hover:underline"
                >
                  View Lead →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
