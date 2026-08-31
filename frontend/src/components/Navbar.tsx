import React from 'react';
import { LayoutDashboard, Users, CalendarCheck, PhoneCall, Bot } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'leads', label: 'Leads CRM', icon: Users },
    { id: 'followups', label: 'Follow-Ups', icon: CalendarCheck },
    { id: 'demo', label: 'AI Voice Demo', icon: Bot },
  ];

  return (
    <header className="bg-white border-b border-gray-100 sticky top-0 z-30 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('dashboard')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-purple-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-purple-500/20">
              <PhoneCall className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-gray-900 to-purple-900 bg-clip-text text-transparent">
                LinguaLead
              </span>
              <span className="hidden sm:inline-block ml-2 px-2 py-0.5 text-xs font-semibold bg-purple-50 text-purple-700 rounded-full border border-purple-100">
                AI Voice CRM
              </span>
            </div>
          </div>

          <nav className="flex items-center space-x-1 sm:space-x-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-sm font-medium transition-all duration-200 ${
                    isActive
                      ? 'bg-purple-50 text-purple-700 shadow-xs'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-purple-600' : 'text-gray-400'}`} />
                  <span className="hidden md:inline">{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};
