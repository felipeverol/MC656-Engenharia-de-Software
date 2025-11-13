const API_BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

function getAuthHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function saveCart(cartName: string = "My Cart") {
  const response = await fetch(`${API_BASE_URL}/cart/save?cart_name=${encodeURIComponent(cartName)}`, {
    method: "POST",
    headers: {
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    if (response.status === 404) throw new Error("Cart not found or empty");
    if (response.status === 401) throw new Error("Unauthorized: token inválido ou ausente");
    throw new Error("Failed to save cart");
  }

  const data = await response.json();
  return data;
}
