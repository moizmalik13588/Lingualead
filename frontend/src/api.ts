import type { LeadListItem, LeadDetail, FollowUp, DashboardStats } from './types';

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

export async function simulateWebhook(fixtureName: string): Promise<any> {
  // We can trigger simulation via backend or send a mock payload to /api/vapi/webhook
  const payload = fixtureName === 'urdu' 
    ? {
        message: {
          type: 'end-of-call-report',
          call: {
            id: `call-demo-${Date.now()}`,
            customer: { number: '+923005554433', name: 'Bilal Ahmed' },
            durationSeconds: 72,
            transcript: "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Bilal: Urdu mein baat karte hain. Mujhe software development outsourced karni hai apni company ke liye. Budget around 300k PKR hai aur timeline next month hai.",
            summary: "Bilal Ahmed wants software development services in Urdu. Budget 300k PKR, timeline next month."
          }
        }
      }
    : {
        message: {
          type: 'end-of-call-report',
          call: {
            id: `call-demo-${Date.now()}`,
            customer: { number: '+14155559988', name: 'Jessica Taylor' },
            durationSeconds: 58,
            transcript: "AI Agent: Hello! Welcome to LinguaLead. English mein baat karein ya Urdu mein? Jessica: Hi, English. We are looking for an AI voice sales agent for our e-commerce store. Very interested, budget is $5,000, need it by end of week.",
            summary: "Jessica Taylor interested in AI voice sales agent for e-commerce store. Budget $5k, urgent timeline end of week."
          }
        }
      };

  const res = await fetch(`${API_BASE}/vapi/webhook`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to simulate webhook');
  return res.json();
}
