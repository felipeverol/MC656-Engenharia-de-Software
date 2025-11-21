import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from "recharts";

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
          <CardTitle className="text-lg">Distribuição de Macronutrientes</CardTitle>
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
        <CardTitle className="text-lg">Macronutrient Balance</CardTitle>
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