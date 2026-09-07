import React, { useState } from 'react';
import { simulateWebhook } from '../api';
import { Bot, CheckCircle, Globe, Play, ArrowRight } from 'lucide-react';

interface CallDemoPageProps {
  onSelectLead: (leadId: number) => void;
  setActiveTab: (tab: string) => void;
}

export const CallDemoPage: React.FC<CallDemoPageProps> = ({ onSelectLead, setActiveTab }) => {
  const [simulating, setSimulating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSimulate = async (language: 'english' | 'urdu') => {
    try {
      setSimulating(true);
      setError(null);
      setResult(null);
      const res = await simulateWebhook(language);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Simulation failed');
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-8 pb-12 max-w-4xl mx-auto">
      {/* Header */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 shadow-xs border border-gray-100 text-center space-y-3">
        <div className="w-14 h-14 rounded-2xl bg-purple-100 text-purple-700 flex items-center justify-center mx-auto shadow-inner">
          <Bot className="w-7 h-7" />
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">AI Voice Calling Agent Demo Simulator</h1>
        <p className="text-sm text-gray-500 max-w-xl mx-auto">
          Test the live end-to-end pipeline without needing a live telephone call. Simulate an inbound Urdu or English customer conversation and watch LinguaLead automatically extract insights and update the CRM.
        </p>
      </div>

      {/* Simulator Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* English Demo */}
        <div className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100 flex flex-col justify-between space-y-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-blue-50 text-blue-700 text-xs font-semibold rounded-full border border-blue-100 flex items-center">
                <Globe className="w-3.5 h-3.5 mr-1" /> English Conversation
              </span>
              <span className="text-xs text-gray-400 font-mono">Duration: 58s</span>
            </div>
            <h3 className="text-lg font-bold text-gray-900">E-commerce Sales Inquiry</h3>
            <p className="text-xs text-gray-600 font-mono bg-gray-50 p-3 rounded-xl border border-gray-100">
              "Hi, we are looking for an AI voice sales agent for our e-commerce store. Budget is $5,000, need it by end of week."
            </p>
          </div>
          <button
            onClick={() => handleSimulate('english')}
            disabled={simulating}
            className="w-full py-3 rounded-xl bg-purple-600 text-white font-semibold text-sm hover:bg-purple-500 transition shadow-md shadow-purple-500/20 flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {simulating ? (
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Simulate English Call</span>
              </>
            )}
          </button>
        </div>

        {/* Urdu Demo */}
        <div className="bg-white rounded-3xl p-6 shadow-xs border border-gray-100 flex flex-col justify-between space-y-6">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-full border border-emerald-100 flex items-center">
                <Globe className="w-3.5 h-3.5 mr-1" /> Urdu / Bilingual
              </span>
              <span className="text-xs text-gray-400 font-mono">Duration: 72s</span>
            </div>
            <h3 className="text-lg font-bold text-gray-900">Auto Parts & Software Inquiry</h3>
            <p className="text-xs text-gray-600 font-mono bg-gray-50 p-3 rounded-xl border border-gray-100">
              "Urdu mein baat karte hain. Mujhe software development outsourced karni hai. Budget 300k PKR hai aur timeline next month hai."
            </p>
          </div>
          <button
            onClick={() => handleSimulate('urdu')}
            disabled={simulating}
            className="w-full py-3 rounded-xl bg-purple-600 text-white font-semibold text-sm hover:bg-purple-500 transition shadow-md shadow-purple-500/20 flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {simulating ? (
              <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Simulate Urdu Call</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Simulation Result Success Box */}
      {result && (
        <div className="bg-emerald-50 border border-emerald-200 rounded-3xl p-6 sm:p-8 space-y-4 animate-fadeIn">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500 text-white flex items-center justify-center shadow-md">
              <CheckCircle className="w-6 h-6" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-emerald-900">Call Successfully Processed & Synced to CRM!</h3>
              <p className="text-xs text-emerald-700">Call ID: {result.call_id}</p>
            </div>
          </div>

          <div className="bg-white rounded-2xl p-4 border border-emerald-100 text-xs text-gray-700 font-mono space-y-1">
            <p><strong>Lead ID:</strong> {result.crm_result?.lead_id}</p>
            <p><strong>Status:</strong> {result.crm_result?.lead_status}</p>
            <p><strong>Qualification:</strong> {result.crm_result?.qualification}</p>
            <p><strong>Follow-Up Created:</strong> {String(result.crm_result?.follow_up_created)}</p>
          </div>

          <div className="flex justify-end pt-2">
            <button
              onClick={() => {
                if (result.crm_result?.lead_id) {
                  onSelectLead(result.crm_result.lead_id);
                } else {
                  setActiveTab('leads');
                }
              }}
              className="px-5 py-2.5 rounded-xl bg-emerald-600 text-white font-semibold text-sm hover:bg-emerald-500 transition shadow-md flex items-center space-x-2"
            >
              <span>View Lead in CRM</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-red-700 text-sm">
          Error: {error}
        </div>
      )}
    </div>
  );
};
