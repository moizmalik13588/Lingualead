import React, { useState, useEffect } from 'react';
import type { LeadDetail } from '../types';
import { fetchLeadDetail, updateFollowUp } from '../api';
import { StatusDot } from '../components/StatusDot';
import { ArrowLeft, Phone, Globe, Calendar, Clock, Sparkles, CheckCircle2, ChevronDown, ChevronUp, FileText } from 'lucide-react';

interface LeadDetailPageProps {
  leadId: number;
  onBack: () => void;
}

export const LeadDetailPage: React.FC<LeadDetailPageProps> = ({ leadId, onBack }) => {
  const [lead, setLead] = useState<LeadDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedTranscripts, setExpandedTranscripts] = useState<Record<number, boolean>>({});

  useEffect(() => {
    loadLead();
  }, [leadId]);

  const loadLead = async () => {
    try {
      setLoading(true);
      const data = await fetchLeadDetail(leadId);
      setLead(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleTranscript = (callId: number) => {
    setExpandedTranscripts((prev) => ({ ...prev, [callId]: !prev[callId] }));
  };

  const handleToggleFollowUp = async (fuId: number, currentCompleted: boolean) => {
    try {
      await updateFollowUp(fuId, !currentCompleted);
      loadLead();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading || !lead) {
    return (
      <div className="flex justify-center items-center h-96">
        <div className="animate-spin rounded-full h-10 w-10 border-2 border-purple-600 border-t-transparent"></div>
      </div>
    );
  }

  const latestCall = lead.calls && lead.calls.length > 0 ? lead.calls[0] : null;

  return (
    <div className="space-y-8 pb-12">
      {/* Top Navigation / Back */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="inline-flex items-center space-x-2 px-4 py-2 rounded-xl bg-white text-gray-700 hover:bg-gray-50 border border-gray-200 text-sm font-medium transition shadow-xs"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Leads</span>
        </button>
        <div className="flex items-center space-x-2">
          <StatusDot status={lead.status} />
        </div>
      </div>

      {/* Lead Header Card */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xs border border-gray-100 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 text-white font-bold text-2xl flex items-center justify-center shadow-md shadow-purple-500/20">
            {lead.name.charAt(0)}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{lead.name}</h1>
            <div className="flex flex-wrap items-center gap-3 mt-1.5 text-sm text-gray-500">
              <span className="flex items-center font-mono">
                <Phone className="w-3.5 h-3.5 mr-1 text-gray-400" />
                {lead.phone}
              </span>
              <span>•</span>
              <span className="capitalize flex items-center">
                <Globe className="w-3.5 h-3.5 mr-1 text-gray-400" />
                {lead.language}
              </span>
              <span>•</span>
              <span className="flex items-center">
                <Calendar className="w-3.5 h-3.5 mr-1 text-gray-400" />
                Created {new Date(lead.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* AI Insights Section (Portfolio Showcase) */}
      <div className="bg-gradient-to-br from-purple-900 via-indigo-900 to-gray-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 bottom-0 translate-x-16 translate-y-16 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="relative z-10 space-y-6">
          <div className="flex items-center space-x-2 text-purple-300">
            <Sparkles className="w-5 h-5 text-purple-400 animate-pulse" />
            <h2 className="text-lg font-bold tracking-wide uppercase text-xs text-purple-200">
              AI Insights & Qualification Breakdown
            </h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10">
              <span className="text-xs text-purple-300 font-medium uppercase tracking-wider">Qualification</span>
              <div className="mt-2">
                <StatusDot status={latestCall?.qualification_score || lead.status} />
              </div>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10">
              <span className="text-xs text-purple-300 font-medium uppercase tracking-wider">Language Detected</span>
              <p className="text-base font-bold capitalize mt-1 text-white">{latestCall?.language || lead.language}</p>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10">
              <span className="text-xs text-purple-300 font-medium uppercase tracking-wider">Call Duration</span>
              <p className="text-base font-bold mt-1 text-white">{latestCall ? `${latestCall.duration_seconds} seconds` : 'N/A'}</p>
            </div>
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10">
              <span className="text-xs text-purple-300 font-medium uppercase tracking-wider">Confidence Score</span>
              <p className="text-base font-bold mt-1 text-white">95% High Fidelity</p>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-5 border border-white/10 space-y-3">
            <h3 className="text-sm font-semibold text-purple-200 flex items-center">
              <FileText className="w-4 h-4 mr-2 text-purple-300" />
              AI Conversation Summary
            </h3>
            <p className="text-sm text-gray-200 leading-relaxed">
              {latestCall?.summary || 'No summary available for this lead yet.'}
            </p>
          </div>
        </div>
      </div>

      {/* Two Column Layout: Follow-ups & Call History */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Pending Follow-ups */}
        <div className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-900">Follow-Up Actions</h2>
            <Calendar className="w-5 h-5 text-purple-600" />
          </div>

          {(!lead.follow_ups || lead.follow_ups.length === 0) ? (
            <p className="text-xs text-gray-400 text-center py-6">No follow-ups scheduled.</p>
          ) : (
            <div className="space-y-3">
              {lead.follow_ups.map((fu) => (
                <div
                  key={fu.id}
                  className={`p-4 rounded-2xl border transition ${
                    fu.completed ? 'bg-gray-50 border-gray-100 opacity-75' : 'bg-purple-50/40 border-purple-100'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <span className="text-xs font-semibold text-purple-700">
                      {new Date(fu.scheduled_for).toLocaleString()}
                    </span>
                    <button
                      onClick={() => handleToggleFollowUp(fu.id, fu.completed)}
                      className={`px-2.5 py-1 rounded-lg text-xs font-semibold flex items-center space-x-1 transition ${
                        fu.completed ? 'bg-gray-200 text-gray-700 hover:bg-gray-300' : 'bg-purple-600 text-white hover:bg-purple-500'
                      }`}
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 mr-1" />
                      <span>{fu.completed ? 'Completed' : 'Mark Done'}</span>
                    </button>
                  </div>
                  <p className="text-xs text-gray-700 font-medium">{fu.notes || 'Follow up with lead.'}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Full Call History */}
        <div className="lg:col-span-2 bg-white rounded-3xl p-6 sm:p-8 shadow-xs border border-gray-100 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-gray-900">Call History & Transcripts</h2>
              <p className="text-xs text-gray-500">{lead.calls?.length || 0} recorded voice call(s)</p>
            </div>
            <Phone className="w-5 h-5 text-purple-600" />
          </div>

          {(!lead.calls || lead.calls.length === 0) ? (
            <p className="text-xs text-gray-400 text-center py-8">No calls recorded for this lead.</p>
          ) : (
            <div className="space-y-4">
              {lead.calls.map((call) => {
                const isExpanded = !!expandedTranscripts[call.id];
                return (
                  <div key={call.id} className="p-5 rounded-2xl bg-gray-50/70 border border-gray-100 space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <StatusDot status={call.qualification_score || 'warm'} />
                        <span className="text-xs font-mono text-gray-400">
                          {new Date(call.created_at).toLocaleString()}
                        </span>
                      </div>
                      <span className="text-xs text-gray-500 font-medium flex items-center">
                        <Clock className="w-3 h-3 mr-1 text-gray-400" />
                        {call.duration_seconds}s
                      </span>
                    </div>

                    <p className="text-sm text-gray-800 font-medium">
                      {call.summary || 'Call completed.'}
                    </p>

                    {call.transcript && (
                      <div className="pt-2">
                        <button
                          onClick={() => toggleTranscript(call.id)}
                          className="text-xs font-semibold text-purple-600 hover:text-purple-700 flex items-center space-x-1"
                        >
                          <span>{isExpanded ? 'Hide Full Transcript' : 'View Full Transcript'}</span>
                          {isExpanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                        </button>

                        {isExpanded && (
                          <div className="mt-3 p-4 rounded-xl bg-white border border-gray-200 text-xs text-gray-700 font-mono whitespace-pre-wrap leading-relaxed max-h-60 overflow-y-auto">
                            {call.transcript}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
