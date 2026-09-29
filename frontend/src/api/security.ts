import { apiRequest } from "./client";
import type { Alert, DashboardSummary, Detection, SecurityEvent } from "../types";

export const getBackendStatus = () =>
  apiRequest<{ status: string; service: string }>("/api/status");

export const getDatabaseStatus = () =>
  apiRequest<{ configured: string; status: string }>("/api/database-status");

export const getDashboardSummary = () =>
  apiRequest<DashboardSummary>("/api/dashboard/summary");

export const getDetections = () =>
  apiRequest<Detection[]>("/api/dashboard/detections");

export const getAlerts = () =>
  apiRequest<Alert[]>("/api/dashboard/alerts");

export const getSecurityEvents = () =>
  apiRequest<SecurityEvent[]>("/api/dashboard/security-events");

export const analyzeNetworkRequest = (input: {
  request_id: string;
  url: string;
  method: string;
  domain: string;
  timestamp: string;
}) =>
  apiRequest<{
    status: string;
    request: typeof input;
    detection: Detection;
    alert: Alert | null;
    security_event: SecurityEvent;
  }>("/api/network-requests", {
    method: "POST",
    body: JSON.stringify(input),
  });
