import { Product, CartResponse } from "@/types/product";

const API_BASE_URL = (import.meta.env.VITE_API_URL || "http://localhost:8000").replace(/\/$/, "");

export async function addProductToCart(barcode: string): Promise<Product> {
  const response = await fetch(`${API_BASE_URL}/add/${barcode}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Product not found");
    }
    throw new Error("Failed to add product to cart");
  }

  const data = await response.json();
  // The API returns the updated cart, we need to fetch the full cart to get the product details
  const cartData = await getCart();
  const addedProduct = cartData.products.find(p => p.code === barcode);

  if (!addedProduct) {
    throw new Error("Product not found in cart after adding");
  }

  return addedProduct;
}

export async function getCart(): Promise<CartResponse> {
  const response = await fetch(`${API_BASE_URL}/cart`);

  if (!response.ok) {
    if (response.status === 404) {
      return { total_items: 0, products: [] };
    }
    throw new Error("Failed to fetch cart");
  }

  const data = await response.json();
  return data.cart;
}

export async function removeProductFromCart(barcode: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/remove/${barcode}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Product not found in cart");
    }
    throw new Error("Failed to remove product from cart");
  }
}

export async function deleteCart(): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/delete/cart`);

  if (!response.ok) {
    throw new Error("Failed to delete cart");
  }
}