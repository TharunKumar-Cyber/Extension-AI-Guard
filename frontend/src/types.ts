export type User = {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
};

export type Detection = {
  result_id: string;
  request_id: string;
  is_malicious: boolean;
  confidence: number;
  threat_type: string;
  explanation: string;
  url?: string;
  domain?: string;
  method?: string;
  timestamp?: string;
};

export type Alert = {
  alert_id: string;
  result_id: string;
  severity: "low" | "medium" | "high" | "critical";
  title: string;
  message: string;
  created_at: string;
  acknowledged: boolean;
};

export type SecurityEvent = {
  event_id: string;
  event_type: string;
  source: string;
  severity: "low" | "medium" | "high" | "critical";
  description: string;
  timestamp: string;
};

export type DashboardSummary = {
  detection_count: number;
  malicious_count: number;
  benign_count: number;
  alert_count: number;
  event_count: number;
  latest_detection: Detection | null;
};