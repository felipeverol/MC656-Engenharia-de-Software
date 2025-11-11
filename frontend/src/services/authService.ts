const API_BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000")
  .replace(/\/$/, "");

export async function registerUser(name: string, email: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Erro ao registrar usuário");
  }

  return response.json();
}

export async function loginUser(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData.toString(),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Falha no login");
  }

  const data = await response.json();
  const token = data.access_token;
  localStorage.setItem("token", token);
  return token;
}

export async function getCurrentUser() {
  const token = localStorage.getItem("token");
  if (!token) throw new Error("Usuário não autenticado");

  const response = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || "Erro ao obter usuário");
  }

  return response.json();
}

export function logoutUser() {
  localStorage.removeItem("token");
}
