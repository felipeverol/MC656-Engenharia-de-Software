import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Trash2, ShoppingCart } from "lucide-react";
import { Product } from "@/types/product";

interface ProductListProps {
  items: Product[];
  onRemoveItem: (barcode: string) => void;
}

export default function ProductList({ items = [], onRemoveItem }: ProductListProps) {
  if (items.length === 0) {
    return (
      <Card className="shadow-lg border-2">
        <CardContent className="pt-6">
          <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
            <ShoppingCart className="h-16 w-16 mb-4 opacity-30" />
            <p className="text-lg font-medium">Seu carrinho está vazio</p>
            <p className="text-sm mt-1">Adicione produtos digitando o código de barras acima</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-lg border-2">
      <CardContent className="pt-6">
        <ScrollArea className="h-[400px] pr-4">
          <div className="space-y-3">
            {items.map((item) => (
              <div
                key={item.code}
                className="flex items-center justify-between p-4 rounded-lg border-2 bg-card hover:bg-accent/50 transition-colors"
              >
                <div className="flex-1">
                  <h3 className="font-semibold text-base">{item.name || "Produto Desconhecido"}</h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    Código de barras: {item.code}
                  </p>
                  <div className="flex gap-4 mt-2 text-xs text-muted-foreground">
                    <span>Carboidratos: {(item.nutriments.carbohydrates || 0).toFixed(1)}g</span>
                    <span>Proteínas: {(item.nutriments.proteins || 0).toFixed(1)}g</span>
                    <span>Gorduras: {(item.nutriments.fat || 0).toFixed(1)}g</span>
                    <span className="font-semibold">{(item.nutriments["energy-kcal"] || 0).toFixed(0)} cal</span>
                  </div>
                </div>
                <Button
                  variant="destructive"
                  size="icon"
                  onClick={() => onRemoveItem(item.code)}
                  className="ml-4 h-9 w-9"
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}