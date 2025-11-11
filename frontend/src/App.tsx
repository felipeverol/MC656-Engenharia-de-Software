import { Suspense } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import ShoppingCart from "./components/shopping-cart/ShoppingCart";
import AuthPage from "./components/auth-page/AuthPage";

function PrivateRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/auth" replace />;
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

        {/* Redireciona qualquer rota inválida pra home */}
        <Route path="*" element={<Navigate to="/home" replace />} />
      </Routes>
    </Suspense>
  );
}