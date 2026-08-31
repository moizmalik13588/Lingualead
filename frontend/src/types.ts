export type Language = 'urdu' | 'english';
export type LeadStatus = 'new' | 'hot' | 'warm' | 'cold' | 'follow_up';
export type QualificationScore = 'hot' | 'warm' | 'cold';

export interface Call {
  id: number;
  lead_id: number;
  transcript?: string;
  summary?: string;
  qualification_score?: QualificationScore;
  duration_seconds: number;
  language: Language;
  created_at: string;
}

export interface FollowUp {
  id: number;
  lead_id: number;
  scheduled_for: string;
  notes?: string;
  completed: boolean;
  created_at: string;
  lead_name?: string;
  lead_phone?: string;
}

export interface LeadListItem {
  id: number;
  name: string;
  phone: string;
  language: Language;
  status: LeadStatus;
  created_at: string;
  last_call_at?: string;
  total_calls: number;
  latest_qualification?: QualificationScore;
}

export interface LeadDetail extends LeadListItem {
  calls: Call[];
  follow_ups: FollowUp[];
}

export interface DashboardStats {
  total_leads: number;
  hot_leads_count: number;
  calls_today_count: number;
  pending_follow_ups_count: number;
  recent_calls: Call[];
  recent_leads: LeadListItem[];
}
