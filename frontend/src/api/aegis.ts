import { apiRequest } from "./client";

export const getAegisWelcome = () => apiRequest<Record<string, unknown>>("/api/aegis/welcome");
export const getAegisStatus = () => apiRequest<Record<string, unknown>>("/api/aegis/status");
export const getAegisKnowledge = () => apiRequest<Record<string, unknown>>("/api/aegis/knowledge");

export const sendAegisMessage = (message: string) =>
  apiRequest<Record<string, unknown>>("/api/aegis/message", {
    method: "POST",
    body: JSON.stringify({ message }),
  });

export const explainAlert = (severity: string, title: string, message: string) =>
  apiRequest<Record<string, unknown>>(
    `/api/aegis/alerts/explain?severity=${encodeURIComponent(severity)}&title=${encodeURIComponent(title)}&message=${encodeURIComponent(message)}`,
  );
