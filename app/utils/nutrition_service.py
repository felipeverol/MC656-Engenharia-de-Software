from app.utils.observer import Observer

class NutritionObserver(Observer):
    def __init__(self):
        self.total_calories = 0

    def update(self, event: str, data: dict):
        if event == "product_added":
            print(f"Atualizando calorias totais após {data['code']}")

        elif event == "product_removed":
            print(f"Recalculando calorias totais após remoção do produto {data['code']}")
        
        elif event == "cart_deleted":
            print("Carrinho deletado, zerando total de calorias.")
            self.total_calories = 0