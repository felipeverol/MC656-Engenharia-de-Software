import { Product, CartResponse } from "@/types/product";

const API_BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

function getAuthHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function addProductToCart(barcode: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/cart/add/${barcode}`, {
    headers: {
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    if (response.status === 404) throw new Error("Produto não encontrado");
    if (response.status === 401) throw new Error("Não autorizado: token inválido ou ausente");
    throw new Error("Falha ao adicionar produto ao carrinho");
  }

  const data = await response.json();

  const cartData = await getCart();
  const addedProduct = cartData.products.find(p => p.code === barcode);

  if (!addedProduct) {
    throw new Error("Produto não encontrado no carrinho após adição");
  }

  return addedProduct;
}

export async function getCart(): Promise<CartResponse> {
  const response = await fetch(`${API_BASE_URL}/cart`, {
    headers: {
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    if (response.status === 404) return { total_items: 0, products: [] };
    if (response.status === 401) throw new Error("Não autorizado: token inválido ou ausente");
    throw new Error("Falha ao buscar carrinho");
  }

  const data = await response.json();
  return data.cart;
}

export async function removeProductFromCart(barcode: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/cart/remove/${barcode}`, {
    headers: {
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    if (response.status === 404) throw new Error("Produto não encontrado no carrinho");
    if (response.status === 401) throw new Error("Não autorizado: token inválido ou ausente");
    throw new Error("Falha ao remover produto do carrinho");
  }
}

export async function deleteCart(): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/cart/delete`, {
    headers: {
      ...getAuthHeaders(),
    },
  });

  if (!response.ok) {
    if (response.status === 401) throw new Error("Não autorizado: token inválido ou ausente");
    throw new Error("Falha ao excluir carrinho");
  }
}