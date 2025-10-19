export interface Product {
  code: string;
  name: string;
  nutriments: {
    carbohydrates: number;
    proteins: number;
    fat: number;
    "energy-kcal": number;
  };
}

export interface CartResponse {
  total_items: number;
  products: Product[];
}