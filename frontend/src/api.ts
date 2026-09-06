import type { LeadListItem, LeadDetail, FollowUp, DashboardStats, AIInsightsOut } from './types';

const API_BASE = 'http://localhost:8000/api';

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const res = await fetch(`${API_BASE}/dashboard/stats`);
  if (!res.ok) throw new Error('Failed to fetch dashboard stats');
  return res.json();
}

export async function fetchLeads(params?: {
  status?: string;
  language?: string;
  qualification?: string;
  search?: string;
}): Promise<LeadListItem[]> {
  const query = new URLSearchParams();
  if (params?.status && params.status !== 'all') query.append('status', params.status);
  if (params?.language && params.language !== 'all') query.append('language', params.language);
  if (params?.qualification && params.qualification !== 'all') query.append('qualification', params.qualification);
  if (params?.search) query.append('search', params.search);

  const res = await fetch(`${API_BASE}/leads?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch leads');
  return res.json();
}

export async function fetchLeadDetail(id: number): Promise<LeadDetail> {
  const res = await fetch(`${API_BASE}/leads/${id}`);
  if (!res.ok) throw new Error('Failed to fetch lead detail');
  return res.json();
}

export async function fetchFollowUps(completed?: boolean): Promise<FollowUp[]> {
  const query = new URLSearchParams();
  if (completed !== undefined) query.append('completed', String(completed));

  const res = await fetch(`${API_BASE}/followups?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch follow-ups');
  return res.json();
}

export async function updateFollowUp(id: number, completed: boolean): Promise<FollowUp> {
  const res = await fetch(`${API_BASE}/followups/${id}?completed=${completed}`, {
    method: 'PATCH',
  });
  if (!res.ok) throw new Error('Failed to update follow-up');
  return res.json();
}

export async function simulateWebhook(language: string): Promise<any> {
  const res = await fetch(`${API_BASE}/demo/simulate-call`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ language }),
  });
  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || 'Failed to simulate call');
  }
  return res.json();
}

export async function fetchAIInsights(): Promise<AIInsightsOut> {
  const res = await fetch(`${API_BASE}/dashboard/ai-insights`);
  if (!res.ok) throw new Error('Failed to fetch AI insights');
  return res.json();
}
