import React, { useEffect, useState } from "react";

interface Product {
  code: string;
  name: string;
  nutriments?: {
    carbohydrates?: number;
    proteins?: number;
    fat?: number;
    "energy-kcal"?: number;
  };
}

interface SavedCart {
  id: number;
  name: string;
  cart_data: Product[];
}

interface UserData {
  name: string;
  email: string;
  id: number;
  carts: SavedCart[];
}

export default function SavedCartsPage() {
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);

  const API = "http://localhost:8000";
  const token = localStorage.getItem("token");

  const loadUserData = async () => {
    try {
      const res = await fetch(`${API}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!res.ok) throw new Error("Erro ao carregar usuário");

      const data = await res.json();
      setUser(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUserData();
  }, []);

  if (loading) return <p>Carregando carrinhos...</p>;
  if (!user) return <p>Erro ao carregar usuário.</p>;

  return (
    <div style={{ padding: 20, maxWidth: 700, margin: "0 auto" }}>
      <p className="text-2xl font-bold">Olá, seus carrinhos salvos:</p>

      {user.carts.length === 0 && <p>Nenhum carrinho salvo.</p>}

      {user.carts.map((cart, index) => (
    <div
        key={cart.id}
        style={{
        background: "white",
        padding: "20px",
        margin: "20px 0",
        borderRadius: "12px",
        boxShadow: "0 4px 10px rgba(0,0,0,0.08)",
        border: "1px solid #e5e7eb",
        }}
    >
    <h2 style={{ marginBottom: "12px", fontSize: "22px" }}>
      {`Carrinho ${index + 1}`}
    </h2>

    {cart.cart_data.length === 0 ? (
      <p style={{ opacity: 0.7 }}>(Carrinho vazio)</p>
    ) : (
      <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
        {cart.cart_data.map((product) => {
        const carbs = product.nutriments?.carbohydrates ?? 0;
        const proteins = product.nutriments?.proteins ?? 0;
        const fat = product.nutriments?.fat ?? 0;
        const calories = product.nutriments?.["energy-kcal"] ?? 0;

        return (
            <div
            key={product.code}
            style={{
                background: "white",
                borderRadius: "10px",
                padding: "16px",
                border: "1px solid #e5e7eb",
                boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
            }}
            >
            {/* Nome */}
            <strong style={{ fontSize: "18px" }}>{product.name}</strong>

            {/* Código */}
            <p style={{ marginTop: "4px", color: "#6b7280" }}>
                Barcode: {product.code}
            </p>

            {/* Nutrição dinâmica */}
            <p style={{ marginTop: "8px", fontSize: "14px", color: "#374151" }}>
                <span style={{ marginRight: "14px" }}>
                Carbs: {carbs}g
                </span>
                <span style={{ marginRight: "14px" }}>
                Protein: {proteins}g
                </span>
                <span style={{ marginRight: "14px" }}>
                Fat: {fat}g
                </span>
                <strong>{calories} cal</strong>
            </p>
            </div>
        );
        })}
      </div>
    )}
  </div>
))}

    </div>
  );
}
