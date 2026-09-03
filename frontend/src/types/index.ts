export interface Lead {
  id: string;
  name: string;
  email: string | null;
  phone: string | null;
  company_name: string | null;
  status: string;
  ai_score: number | null;
  ai_summary: string | null;
  deal_probability: number | null;
  next_best_action: string | null;
  created_at: string;
}

export interface DashboardSummary {
  revenue: number;
  qualified_leads: number;
  conversion_rate: number;
  avg_ai_score: number | null;
  pipeline: number;
  total_leads: number;
}
