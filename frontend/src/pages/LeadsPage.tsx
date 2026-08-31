import React, { useState, useEffect } from 'react';
import type { LeadListItem } from '../types';
import { fetchLeads } from '../api';
import { StatusDot } from '../components/StatusDot';
import { Search, Globe, Phone, Users } from 'lucide-react';

interface LeadsPageProps {
  onSelectLead: (leadId: number) => void;
}

export const LeadsPage: React.FC<LeadsPageProps> = ({ onSelectLead }) => {
  const [leads, setLeads] = useState<LeadListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [languageFilter, setLanguageFilter] = useState<string>('all');
  const [qualificationFilter, setQualificationFilter] = useState<string>('all');

  useEffect(() => {
    loadLeads();
  }, [statusFilter, languageFilter, qualificationFilter]);

  const loadLeads = async () => {
    try {
      setLoading(true);
      const data = await fetchLeads({
        status: statusFilter,
        language: languageFilter,
        qualification: qualificationFilter,
        search: search.trim() || undefined,
      });
      setLeads(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadLeads();
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header & Search / Filters */}
      <div className="bg-white rounded-2xl p-6 shadow-xs border border-gray-100 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Leads CRM Pipeline</h1>
            <p className="text-sm text-gray-500">Manage and filter all voice-qualified leads</p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="px-3 py-1 bg-purple-50 text-purple-700 font-semibold text-xs rounded-full border border-purple-100">
              {leads.length} Total Leads
            </span>
          </div>
        </div>

        {/* Filter Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
          {/* Search */}
          <form onSubmit={handleSearchSubmit} className="relative">
            <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3.5" />
            <input
              type="text"
              placeholder="Search by name or phone..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && loadLeads()}
              className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500"
            />
          </form>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2.5 rounded-xl border border-gray-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500"
          >
            <option value="all">All Statuses</option>
            <option value="hot">Hot</option>
            <option value="warm">Warm</option>
            <option value="cold">Cold</option>
            <option value="new">New</option>
          </select>

          {/* Language Filter */}
          <select
            value={languageFilter}
            onChange={(e) => setLanguageFilter(e.target.value)}
            className="px-4 py-2.5 rounded-xl border border-gray-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500"
          >
            <option value="all">All Languages</option>
            <option value="english">English</option>
            <option value="urdu">Urdu / Bilingual</option>
          </select>

          {/* Qualification Filter */}
          <select
            value={qualificationFilter}
            onChange={(e) => setQualificationFilter(e.target.value)}
            className="px-4 py-2.5 rounded-xl border border-gray-200 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-purple-500/20 focus:border-purple-500"
          >
            <option value="all">All Qualifications</option>
            <option value="hot">Hot Score</option>
            <option value="warm">Warm Score</option>
            <option value="cold">Cold Score</option>
          </select>
        </div>
      </div>

      {/* Leads Table (Desktop) & Cards (Mobile) */}
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
        </div>
      ) : leads.length === 0 ? (
        <div className="bg-white rounded-2xl p-12 text-center border border-gray-100">
          <Users className="w-12 h-12 text-gray-300 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-gray-800">No leads found</h3>
          <p className="text-sm text-gray-500 mt-1">Try adjusting your filters or search query.</p>
        </div>
      ) : (
        <>
          {/* Desktop Table */}
          <div className="hidden md:block bg-white rounded-2xl shadow-xs border border-gray-100 overflow-hidden">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50/70 border-b border-gray-100 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  <th className="py-4 px-6">Lead Name</th>
                  <th className="py-4 px-6">Qualification</th>
                  <th className="py-4 px-6">Language</th>
                  <th className="py-4 px-6">Phone</th>
                  <th className="py-4 px-6">Total Calls</th>
                  <th className="py-4 px-6">Created</th>
                  <th className="py-4 px-6 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 text-sm">
                {leads.map((lead) => (
                  <tr
                    key={lead.id}
                    onClick={() => onSelectLead(lead.id)}
                    className="hover:bg-purple-50/30 transition cursor-pointer group"
                  >
                    <td className="py-4 px-6 font-semibold text-gray-900 flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 font-bold flex items-center justify-center text-sm shadow-xs">
                        {lead.name.charAt(0)}
                      </div>
                      <div>
                        <div className="group-hover:text-purple-700 transition">{lead.name}</div>
                        <div className="text-xs text-gray-400 font-normal">ID: #{lead.id}</div>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <StatusDot status={lead.latest_qualification || lead.status} />
                    </td>
                    <td className="py-4 px-6 capitalize text-gray-600">
                      <span className="inline-flex items-center space-x-1">
                        <Globe className="w-3.5 h-3.5 text-gray-400 mr-1" />
                        {lead.language}
                      </span>
                    </td>
                    <td className="py-4 px-6 font-mono text-xs text-gray-600">
                      <span className="inline-flex items-center space-x-1">
                        <Phone className="w-3 h-3 text-gray-400 mr-1" />
                        {lead.phone}
                      </span>
                    </td>
                    <td className="py-4 px-6 font-medium text-gray-700">{lead.total_calls}</td>
                    <td className="py-4 px-6 text-xs text-gray-500">
                      {new Date(lead.created_at).toLocaleDateString()}
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectLead(lead.id);
                        }}
                        className="px-3 py-1.5 rounded-lg bg-gray-50 text-gray-600 group-hover:bg-purple-600 group-hover:text-white transition text-xs font-semibold"
                      >
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Mobile Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 md:hidden">
            {leads.map((lead) => (
              <div
                key={lead.id}
                onClick={() => onSelectLead(lead.id)}
                className="bg-white rounded-2xl p-5 shadow-xs border border-gray-100 hover:shadow-md transition cursor-pointer space-y-4"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-xl bg-purple-100 text-purple-700 font-bold flex items-center justify-center text-sm">
                      {lead.name.charAt(0)}
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900">{lead.name}</h3>
                      <p className="text-xs text-gray-500 font-mono">{lead.phone}</p>
                    </div>
                  </div>
                  <StatusDot status={lead.latest_qualification || lead.status} />
                </div>
                <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-gray-50">
                  <span className="capitalize flex items-center">
                    <Globe className="w-3.5 h-3.5 mr-1 text-gray-400" /> {lead.language}
                  </span>
                  <span>{lead.total_calls} call(s)</span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};
