import { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { LeadsPage } from './pages/LeadsPage';
import { LeadDetailPage } from './pages/LeadDetailPage';
import { FollowUpsPage } from './pages/FollowUpsPage';
import { CallDemoPage } from './pages/CallDemoPage';
import { fetchDashboardStats } from './api';
import type { DashboardStats } from './types';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [selectedLeadId, setSelectedLeadId] = useState<number | null>(null);
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loadingStats, setLoadingStats] = useState<boolean>(true);

  useEffect(() => {
    if (activeTab === 'dashboard') {
      loadStats();
    }
  }, [activeTab]);

  const loadStats = async () => {
    try {
      setLoadingStats(true);
      const data = await fetchDashboardStats();
      setStats(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingStats(false);
    }
  };

  const handleSelectLead = (leadId: number) => {
    setSelectedLeadId(leadId);
    setActiveTab('lead-detail');
  };

  return (
    <div className="min-h-screen bg-[#f8f9fc] text-gray-900 font-sans selection:bg-purple-500 selection:text-white">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        {activeTab === 'dashboard' && (
          <DashboardPage
            stats={stats}
            loading={loadingStats}
            onSelectLead={handleSelectLead}
            setActiveTab={setActiveTab}
          />
        )}
        {activeTab === 'leads' && (
          <LeadsPage onSelectLead={handleSelectLead} />
        )}
        {activeTab === 'lead-detail' && selectedLeadId && (
          <LeadDetailPage leadId={selectedLeadId} onBack={() => setActiveTab('leads')} />
        )}
        {activeTab === 'followups' && (
          <FollowUpsPage onSelectLead={handleSelectLead} />
        )}
        {activeTab === 'demo' && (
          <CallDemoPage onSelectLead={handleSelectLead} setActiveTab={setActiveTab} />
        )}
      </main>
    </div>
  );
}

export default App;
