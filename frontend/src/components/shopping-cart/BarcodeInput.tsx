import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Loader2, Plus } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";

interface BarcodeInputProps {
  onAddProduct: (barcode: string) => Promise<void>;
}

export default function BarcodeInput({ onAddProduct }: BarcodeInputProps) {
  const [barcode, setBarcode] = useState("");
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!barcode.trim()) {
      toast({
        title: "Invalid Barcode",
        description: "Please enter a valid barcode",
        variant: "destructive",
      });
      return;
    }

    setLoading(true);
    try {
      await onAddProduct(barcode);
      setBarcode("");
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to add product",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="shadow-lg border-2">
      <CardContent className="pt-6">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <Input
            type="text"
            placeholder="Enter barcode..."
            value={barcode}
            onChange={(e) => setBarcode(e.target.value)}
            disabled={loading}
            className="flex-1 h-11 text-base"
          />
          <Button 
            type="submit" 
            disabled={loading}
            className="h-11 px-6 font-semibold"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Adding...
              </>
            ) : (
              <>
                <Plus className="mr-2 h-4 w-4" />
                Add Product
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
