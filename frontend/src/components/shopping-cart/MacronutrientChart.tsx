import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";
import { BarChart3 } from "lucide-react";

interface MacronutrientChartProps {
  carbs: number;
  proteins: number;
  fats: number;
}

export default function MacronutrientChart({
  carbs,
  proteins,
  fats,
}: MacronutrientChartProps) {
  const data = [
    { name: "Carboidratos", value: carbs, color: "#3b82f6" },
    { name: "Proteínas", value: proteins, color: "#ef4444" },
    { name: "Gorduras", value: fats, color: "#eab308" },
  ].filter((item) => item.value > 0);

  const total = carbs + proteins + fats;

  if (total === 0) {
    return (
      <Card className="shadow-lg border-2">
        <CardHeader>
          <div className="flex items-center gap-2 mb-6">
            <BarChart3 className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-semibold text-primary">
              Distribuição de Macronutrientes
            </h2>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-[300px] text-muted-foreground">
            <p>Adicione produtos para ver a distribuição de macronutrientes</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="shadow-lg border-2">
      <CardHeader>
        <div className="flex items-center gap-2 mb-6">
          <BarChart3 className="h-6 w-6 text-primary" />
          <h2 className="text-2xl font-semibold text-primary">
            Distribuição de Macronutrientes
          </h2>
        </div>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry: any) => `${entry.name}: ${((entry.percent || 0) * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value: number) => `${value.toFixed(1)}g`}
              contentStyle={{
                backgroundColor: "hsl(var(--card))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "8px",
              }}
            />
            <Legend
              verticalAlign="bottom"
              height={36}
              iconType="circle"
            />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}