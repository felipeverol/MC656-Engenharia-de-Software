from app.utils import product
from app.utils.observer import Observer
import requests

URL = "https://world.openfoodfacts.net/api/v2/product/{barcode}?fields=code,product_name,nutriments"

class Cart:
    def __init__(self):
        self._products = []
        self._observers = []  # lista de observadores

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def _notify(self, event: str, data: dict):
        for observer in self._observers:
            observer.update(event, data)

    @property
    def products(self):
        return self._products

    def add_product(self, barcode: str):
        response = requests.get(URL.format(barcode=barcode))
        
        if response.status_code == 200:
            product_data = response.json().get('product', {})
            
            item = product.Product(
                code=product_data.get('code'),
                name=product_data.get('product_name'),
                nutriments=product_data.get('nutriments')
            )
            
            self._products.append(item)
            self._notify("product_added", {"code": barcode})
            return item
        
        return None

    def list_items(self):
        data = {
            "total_items": len(self._products),
            "products": [
                {
                    "code": p.code,
                    "name": p.name,
                    "nutriments": p.nutriments
                }
                for p in self._products
            ]
        }
        return data
    
    def remove_item(self, barcode: str):
        for i, product in enumerate(self._products):
            if product.code == barcode:
                del self._products[i]
                return True
        self._notify("product_removed", {"code": barcode})
        return False

    def delete_cart(self):
        self._products = []
        self._total_items = 0
        self._notify("cart_deleted", {"message": "Cart has been cleared"})
        return True