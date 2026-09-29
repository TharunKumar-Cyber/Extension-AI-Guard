import { apiRequest, setToken } from "./client";
import type { User } from "../types";

export async function registerUser(input: {
  username: string;
  email: string;
  password: string;
}) {
  return apiRequest<{ status: string; user: User }>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(input),
  });
}

export async function loginUser(input: { email: string; password: string }) {
  const result = await apiRequest<{
    status: string;
    access_token?: string;
    user?: User;
    message?: string;
  }>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(input),
  });

  if (!result.access_token || !result.user) {
    throw new Error(result.message ?? "Authentication failed.");
  }

  setToken(result.access_token);
  return result.user;
}
