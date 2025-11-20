from typing import Dict
from app.utils.observer import Observer
from app.utils.product_service import ProductService

user_carts: Dict[int, 'Cart'] = {}

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
        item = ProductService.fetch_product(barcode)
        if item:
            self._products.append(item)
            self._notify("product_added", {"code": barcode})
            return item
        return None

    def list_items(self):
        data = {
            "total_items": len(self._products),
            "products": [p.to_dict() for p in self._products]
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
        self._notify("cart_deleted", {"message": "Cart has been cleared"})
        return True