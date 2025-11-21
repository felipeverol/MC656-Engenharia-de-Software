import { Suspense } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import ShoppingCart from "./components/shopping-cart/ShoppingCart";
import AuthPage from "./components/auth-page/AuthPage";
import SavedCartPage from "./components/saved-cart-page/SavedCartPage";

function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return Date.now() >= payload.exp * 1000;
  } catch {
    return true;
  }
}

function PrivateRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem("token");

  if (!token || isTokenExpired(token)) {
    localStorage.removeItem("token");
    return <Navigate to="/auth" replace />;
  }

  return children;
}

export default function App() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <Routes>
        {/* Página de login e registro */}
        <Route path="/auth" element={<AuthPage />} />

        {/* Página principal (carrinho) — protegida por autenticação */}
        <Route
          path="/home"
          element={
            <PrivateRoute>
              <ShoppingCart />
            </PrivateRoute>
          }
        />

        {/* Página de salvamento do carrinho */}
        <Route
          path="/saved-carts"
          element={
            <PrivateRoute>
              <SavedCartPage />
            </PrivateRoute>
          }
        />

        {/* Redireciona qualquer rota inválida pra home */}
        <Route path="*" element={<Navigate to="/home" replace />} />
      </Routes>
    </Suspense>
  );
}