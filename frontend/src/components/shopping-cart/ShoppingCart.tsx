import { useState, useMemo, useEffect } from "react";
import { Product } from "@/types/product";
import { saveCart } from "@/services/cartService";
import {
  addProductToCart,
  getCart,
  removeProductFromCart,
} from "@/services/productService";
import { getCurrentUser } from "@/services/authService";
import BarcodeInput from "@/components/shopping-cart/BarcodeInput";
import ProductList from "@/components/shopping-cart/ProductList";
import NutritionalSummary from "@/components/shopping-cart/NutritionalSummary";
import MacronutrientChart from "@/components/shopping-cart/MacronutrientChart";
import { Toaster } from "@/components/ui/toaster";
import { useToast } from "@/components/ui/use-toast";
import { ShoppingBasket, AlertCircle, Settings2, Mail } from "lucide-react";

// --- 1. Helper para os Sliders de Limite ---
interface LimitControlProps {
  label: string;
  value: number;
  currentTotal: number;
  max: number;
  unit: string;
  onChange: (val: number) => void;
}

const LimitControl = ({
  label,
  value,
  currentTotal,
  max,
  unit,
  onChange,
}: LimitControlProps) => {
  const isExceeded = currentTotal > value;

  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <label className="text-sm font-medium text-slate-700 flex items-center gap-2">
          {label}
          {isExceeded && (
            <span className="text-xs text-red-500 font-bold">(Excedido!)</span>
          )}
        </label>
        <span className="text-sm text-muted-foreground">
          Limite: {value}
          {unit}
        </span>
      </div>
      <input
        type="range"
        min="0"
        max={max}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className={`w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary 
          ${isExceeded ? "accent-red-500" : ""}`}
      />
      <div className="flex justify-between text-xs text-slate-500">
        <span>
          Atual:{" "}
          <span className={isExceeded ? "text-red-600 font-bold" : ""}>
            {currentTotal.toFixed(1)}
            {unit}
          </span>
        </span>
        <span>
          Máx: {max}
          {unit}
        </span>
      </div>
    </div>
  );
};

// --- 2. Helper para Gerar HTML do E-mail ---
const generateEmailHtml = (userName: string, items: Product[], totals: any) => {
  const itemsList = items
    .map(
      (item) =>
        `<li style="margin-bottom: 5px;">
        <strong>${item.name}</strong>: ${item.nutriments["energy-kcal"] || 0
        } kcal
    </li>`
    )
    .join("");

  return `
    <div style="font-family: Arial, sans-serif; color: #333;">
      <h1>Olá, ${userName}!</h1>
      <p>Obrigado por usar o Smart Shopping Cart. Aqui está o resumo da sua compra salva:</p>
      
      <h3>🛒 Itens no Carrinho:</h3>
      <ul>${itemsList}</ul>
      
      <hr style="margin: 20px 0; border: 1px solid #eee;" />
      
      <h3>📊 Resumo Nutricional Total:</h3>
      <p><strong>Calorias:</strong> ${totals.calories.toFixed(0)} kcal</p>
      <p><strong>Carboidratos:</strong> ${totals.carbs.toFixed(1)}g</p>
      <p><strong>Proteínas:</strong> ${totals.proteins.toFixed(1)}g</p>
      <p><strong>Gorduras:</strong> ${totals.fats.toFixed(1)}g</p>
      
      <p style="font-size: 12px; color: #888; margin-top: 30px;">Este é um e-mail automático do seu Smart Cart.</p>
    </div>
  `;
};

// --- Componente Principal ---
export default function ShoppingCart() {
  const [cartItems, setCartItems] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  // Estado para "Enviando E-mail" (para evitar cliques duplos e mostrar feedback)
  const [isSaving, setIsSaving] = useState(false);

  const { toast } = useToast();

  // Estado dos Limites
  const [limits, setLimits] = useState({
    calories: 2000,
    carbs: 300,
    proteins: 150,
    fats: 70,
  });

  useEffect(() => {
    loadCart();
  }, []);

  const loadCart = async () => {
    try {
      const cartData = await getCart();
      setCartItems(cartData.products);
    } catch (error) {
      console.error("Failed to load cart:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddProduct = async (barcode: string) => {
    try {
      const product = await addProductToCart(barcode);
      await loadCart();
      toast({
        title: "Produto Adicionado",
        description: `${product.name} foi adicionado ao seu carrinho`,
      });
    } catch (error) {
      throw error;
    }
  };

  const handleRemoveItem = async (barcode: string) => {
    const item = cartItems.find((item) => item.code === barcode);
    try {
      await removeProductFromCart(barcode);
      await loadCart();
      if (item) {
        toast({
          title: "Produto Removido",
          description: `${item.name} foi removido do seu carrinho`,
        });
      }
    } catch (error) {
      toast({
        title: "Erro",
        description:
          error instanceof Error ? error.message : "Falha ao remover produto",
        variant: "destructive",
      });
    }
  };

  // --- Cálculos Nutricionais ---
  const nutritionalTotals = useMemo(() => {
    return cartItems.reduce(
      (totals, item) => ({
        carbs: totals.carbs + (item.nutriments.carbohydrates || 0),
        proteins: totals.proteins + (item.nutriments.proteins || 0),
        fats: totals.fats + (item.nutriments.fat || 0),
        calories: totals.calories + (item.nutriments["energy-kcal"] || 0),
      }),
      { carbs: 0, proteins: 0, fats: 0, calories: 0 }
    );
  }, [cartItems]);

  // --- Verificação de Limites ---
  const hasExceededLimits = useMemo(() => {
    return (
      nutritionalTotals.calories > limits.calories ||
      nutritionalTotals.carbs > limits.carbs ||
      nutritionalTotals.proteins > limits.proteins ||
      nutritionalTotals.fats > limits.fats
    );
  }, [nutritionalTotals, limits]);

  // --- Função Principal de Salvar e Enviar ---
  const handleSaveCart = async () => {
    if (hasExceededLimits) {
      toast({
        title: "Limites Excedidos",
        description: "Por favor, ajuste seu carrinho ou limites antes de salvar.",
        variant: "destructive",
      });
      return;
    }

    setIsSaving(true);

    try {
      // 1. Salva o carrinho no banco de dados
      const result = await saveCart("My Smart Cart");

      // 2. Pega dados do usuário logado
      const user = await getCurrentUser(); // { name: "Pedro", email: "...", ... }

      if (user && user.email) {
        // 3. Gera o corpo do email
        const htmlBody = generateEmailHtml(
          user.name,
          cartItems,
          nutritionalTotals
        );

        // 4. Chama API Route para enviar o email de verdade
        // Nota: Vamos criar este endpoint '/api/send-email' no próximo passo
        const emailResponse = await fetch("http://localhost:8000/email/send", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            to: user.email,
            subject: "Resumo do seu Smart Cart 🛒",
            html: htmlBody,
          }),
        });

        if (!emailResponse.ok) {
          console.warn("Email failed to send but cart was saved");
          throw new Error("Cart saved, but email failed.");
        }

        toast({
          title: "Sucesso! ✅",
          description: `Carrinho salvo e resumo enviado para ${user.email}`,
        });
      } else {
        toast({
          title: "Carrinho Salvo",
          description: "Carrinho salvo (Nenhum e-mail encontrado para o usuário).",
        });
      }
    } catch (error) {
      console.error(error);
      toast({
        title:
          error instanceof Error && error.message.includes("email")
            ? "Aviso"
            : "Erro",
        description:
          error instanceof Error ? error.message : "Algo deu errado",
        variant:
          error instanceof Error && error.message.includes("email")
            ? "default"
            : "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <ShoppingBasket className="h-16 w-16 text-primary mx-auto mb-4 animate-pulse" />
          <p className="text-lg text-muted-foreground">Carregando carrinho...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header Unificado e Corrigido */}
        <div className="relative mb-8 flex items-center justify-center">
          {/* Título centralizado */}
          <div className="flex flex-col items-center">
            <button
              onClick={() => (window.location.href = "http://localhost:5173/home")}
            >
              <div className="flex items-center gap-3">
                <ShoppingBasket className="h-10 w-10 text-primary" />
                <h1 className="text-4xl font-bold text-primary">Smart Shopping Cart</h1>
              </div>
            </button>
            <p className="text-muted-foreground text-lg">
              Acompanhe sua nutrição a cada leitura
            </p>
          </div>
        </div>

        {/* Main Content */}
        <div className="space-y-6">
          <BarcodeInput onAddProduct={handleAddProduct} />
          <ProductList items={cartItems} onRemoveItem={handleRemoveItem} />

          {/* Summary no topo ocupando a largura toda */}
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4 text-primary">
              Resumo Nutricional
            </h2>

            <NutritionalSummary
              totalCarbs={nutritionalTotals.carbs}
              totalProteins={nutritionalTotals.proteins}
              totalFats={nutritionalTotals.fats}
              totalCalories={nutritionalTotals.calories}
            />
          </div>

          {/* Grid: Chart (esquerda) e Limits (direita) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

            {/* Chart */}
            <MacronutrientChart
              carbs={nutritionalTotals.carbs}
              proteins={nutritionalTotals.proteins}
              fats={nutritionalTotals.fats}
            />

            {/* Limits */}
            <div className="bg-white p-6 rounded-xl shadow-sm border h-fit">
              <div className="flex items-center gap-2 mb-6">
                <Settings2 className="h-6 w-6 text-primary" />
                <h2 className="text-2xl font-semibold text-primary">
                  Limites Nutricionais
                </h2>
              </div>

              <div className="space-y-6">
                <LimitControl
                  label="Máx Calorias"
                  value={limits.calories}
                  currentTotal={nutritionalTotals.calories}
                  max={4000}
                  unit="kcal"
                  onChange={(val) => setLimits((prev) => ({ ...prev, calories: val }))}
                />
                <LimitControl
                  label="Máx Carboidratos"
                  value={limits.carbs}
                  currentTotal={nutritionalTotals.carbs}
                  max={500}
                  unit="g"
                  onChange={(val) => setLimits((prev) => ({ ...prev, carbs: val }))}
                />
                <LimitControl
                  label="Máx Proteínas"
                  value={limits.proteins}
                  currentTotal={nutritionalTotals.proteins}
                  max={300}
                  unit="g"
                  onChange={(val) => setLimits((prev) => ({ ...prev, proteins: val }))}
                />
                <LimitControl
                  label="Máx Gorduras"
                  value={limits.fats}
                  currentTotal={nutritionalTotals.fats}
                  max={150}
                  unit="g"
                  onChange={(val) => setLimits((prev) => ({ ...prev, fats: val }))}
                />
              </div>

              {hasExceededLimits && (
                <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                  <AlertCircle className="h-5 w-5 text-red-600 mt-0.5" />
                  <div>
                    <p className="font-medium text-red-800">Limites Excedidos</p>
                    <p className="text-sm text-red-600">
                      Você não pode salvar ou enviar e-mail até que os limites sejam respeitados.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Botões de ação: Ver carrinhos + Salvar */}
          <div className="flex flex-col md:flex-row justify-center items-center gap-4 mt-8">
            {/* Botão Salvar */}
            <button
              onClick={handleSaveCart}
              disabled={hasExceededLimits || isSaving}
              className={`px-8 py-4 rounded-xl font-bold text-lg transition-all shadow-lg flex items-center gap-3
      ${hasExceededLimits
                  ? "bg-slate-300 text-slate-500 cursor-not-allowed"
                  : "bg-primary text-white hover:bg-primary/90 hover:scale-105 active:scale-95"
                }`}
            >
              {isSaving ? (
                <>Enviando...</>
              ) : hasExceededLimits ? (
                <>Limites Excedidos 🚫</>
              ) : (
                <>
                  <Mail className="w-5 h-5" />
                  Salvar e Enviar E-mail
                </>
              )}
            </button>

            {/* Botão Ver Carrinhos */}
            <button
              onClick={() =>
                (window.location.href = "http://localhost:5173/saved-carts")
              }
              className="px-8 py-4 rounded-xl font-bold text-lg bg-slate-200 text-slate-800 
               hover:bg-slate-300 transition-all shadow flex items-center gap-3"
            >
              📁 Ver meus carrinhos salvos
            </button>
          </div>

          {cartItems.length === 0 && (
            <div className="mt-8 text-center text-sm text-muted-foreground bg-card p-6 rounded-lg border-2 shadow-lg">
              <p className="font-medium mb-2">
                Escaneie qualquer código de barras para começar!
              </p>
              <p className="text-xs">
                O app buscará dados do produto no Open Food Facts
              </p>
            </div>
          )}
        </div>
        <Toaster />
      </div>
    </div>
  );
}