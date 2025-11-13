import { useState, useMemo, useEffect } from "react";
import { Product } from "@/types/product";
import { saveCart } from "@/services/cartService";
import { addProductToCart, getCart, removeProductFromCart } from "@/services/productService";
import BarcodeInput from "@/components/shopping-cart/BarcodeInput";
import ProductList from "@/components/shopping-cart/ProductList";
import NutritionalSummary from "@/components/shopping-cart/NutritionalSummary";
import MacronutrientChart from "@/components/shopping-cart/MacronutrientChart";
import { Toaster } from "@/components/ui/toaster";
import { useToast } from "@/components/ui/use-toast";
import { ShoppingBasket } from "lucide-react";

export default function ShoppingCart() {
  const [cartItems, setCartItems] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  // Load cart on mount
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
      
      // Reload cart to get updated state
      await loadCart();

      toast({
        title: "Product Added",
        description: `${product.name} has been added to your cart`,
      });
    } catch (error) {
      throw error;
    }
  };

  const handleRemoveItem = async (barcode: string) => {
    const item = cartItems.find((item) => item.code === barcode);
    
    try {
      await removeProductFromCart(barcode);
      
      // Reload cart to get updated state
      await loadCart();
      
      if (item) {
        toast({
          title: "Product Removed",
          description: `${item.name} has been removed from your cart`,
        });
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to remove product",
        variant: "destructive",
      });
    }
  };

  const handleSaveCart = async () => {
  try {
    const result = await saveCart("My Smart Cart");

    toast({
      title: "Cart Saved ✅",
      description: result.msg || "Your cart has been successfully saved!",
    });
  } catch (error) {
    toast({
      title: "Error",
      description: error instanceof Error ? error.message : "Something went wrong",
      variant: "destructive",
    });
  }
};

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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center">
        <div className="text-center">
          <ShoppingBasket className="h-16 w-16 text-primary mx-auto mb-4 animate-pulse" />
          <p className="text-lg text-muted-foreground">Loading cart...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4 md:p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="flex items-center justify-center gap-3 mb-3">
            <ShoppingBasket className="h-10 w-10 text-primary" />
            <h1 className="text-4xl font-bold text-primary">Smart Shopping Cart</h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Track your nutrition with every scan
          </p>
        </div>

        {/* Main Content */}
        <div className="space-y-6">
          {/* Barcode Input */}
          <BarcodeInput onAddProduct={handleAddProduct} />

          {/* Product List */}
          <ProductList items={cartItems} onRemoveItem={handleRemoveItem} />

          {/* Nutritional Summary */}
          <div>
            <h2 className="text-2xl font-semibold mb-4 text-primary">
              Nutritional Summary
            </h2>
            <NutritionalSummary
              totalCarbs={nutritionalTotals.carbs}
              totalProteins={nutritionalTotals.proteins}
              totalFats={nutritionalTotals.fats}
              totalCalories={nutritionalTotals.calories}
            />
          </div>

          {/* Macronutrient Chart */}
          <MacronutrientChart
            carbs={nutritionalTotals.carbs}
            proteins={nutritionalTotals.proteins}
            fats={nutritionalTotals.fats}
          />
        </div>

        <div className="flex justify-center mt-8">
          <button
            onClick={handleSaveCart}
            className="px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-primary/90 transition-colors shadow-md"
          >
            Save Cart
          </button>
        </div>

        {/* Helper Text */}
        {cartItems.length === 0 && (
          <div className="mt-8 text-center text-sm text-muted-foreground bg-card p-6 rounded-lg border-2 shadow-lg">
            <p className="font-medium mb-2">Scan any product barcode to get started!</p>
            <p className="text-xs">The app will fetch product data from Open Food Facts</p>
          </div>
        )}
      </div>
      <Toaster />
    </div>
  );
}