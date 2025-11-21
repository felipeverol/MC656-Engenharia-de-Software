const API_BASE_URL = (
  import.meta.env.VITE_API_URL || "http://localhost:8000"
).replace(/\/$/, "");

export function getAuthHeaders() {
  // 1. Recupera o token do LocalStorage (verifique se a chave é 'token' ou 'access_token')
  const token = localStorage.getItem("token");

  // 2. Se tiver token, retorna o cabeçalho formatado
  if (token) {
    return {
      Authorization: `Bearer ${token}`, // <--- O "Bearer " com espaço é OBRIGATÓRIO
      "Content-Type": "application/json",
    };
  }

  // 3. Se não tiver, retorna objeto vazio (vai dar erro 401, mas evita crash no JS)
  return {
    "Content-Type": "application/json",
  };
}

export async function saveCart(cartName: string = "Meu Carrinho") {
  console.log("Tentando salvar carrinho...");
  console.log("Headers enviados:", getAuthHeaders());
  const response = await fetch(
    `${API_BASE_URL}/cart/save?cart_name=${encodeURIComponent(cartName)}`,
    {
      method: "POST",
      headers: {
        ...getAuthHeaders(),
      },
    }
  );

  if (!response.ok) {
    if (response.status === 404) throw new Error("Carrinho não encontrado ou vazio");
    if (response.status === 401)
      throw new Error("Não autorizado: token inválido ou ausente");
    throw new Error("Falha ao salvar carrinho");
  }

  const data = await response.json();
  return data;
}
