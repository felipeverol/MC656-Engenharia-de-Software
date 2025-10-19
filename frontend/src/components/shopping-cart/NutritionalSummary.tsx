import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Apple, Beef, Droplet, Flame } from "lucide-react";

interface NutritionalSummaryProps {
  totalCarbs: number;
  totalProteins: number;
  totalFats: number;
  totalCalories: number;
}

export default function NutritionalSummary({
  totalCarbs,
  totalProteins,
  totalFats,
  totalCalories,
}: NutritionalSummaryProps) {
  const stats = [
    {
      label: "Carbohydrates",
      value: totalCarbs,
      unit: "g",
      icon: Apple,
      color: "text-blue-600",
      bgColor: "bg-blue-50",
    },
    {
      label: "Proteins",
      value: totalProteins,
      unit: "g",
      icon: Beef,
      color: "text-red-600",
      bgColor: "bg-red-50",
    },
    {
      label: "Fats",
      value: totalFats,
      unit: "g",
      icon: Droplet,
      color: "text-yellow-600",
      bgColor: "bg-yellow-50",
    },
    {
      label: "Calories",
      value: totalCalories,
      unit: "kcal",
      icon: Flame,
      color: "text-orange-600",
      bgColor: "bg-orange-50",
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat) => {
        const Icon = stat.icon;
        return (
          <Card key={stat.label} className="shadow-lg border-2 overflow-hidden">
            <CardHeader className={`pb-3 ${stat.bgColor}`}>
              <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                <Icon className={`h-4 w-4 ${stat.color}`} />
                {stat.label}
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-4">
              <div className="flex items-baseline gap-1">
                <span className="text-3xl font-bold">{stat.value.toFixed(1)}</span>
                <span className="text-sm text-muted-foreground font-medium">{stat.unit}</span>
              </div>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
