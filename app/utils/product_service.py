import requests
from app.utils.product import Product

URL = "https://world.openfoodfacts.net/api/v2/product/{barcode}?fields=code,product_name,nutriments"

class ProductService:
    @staticmethod
    def fetch_product(barcode: str) -> Product:
        response = requests.get(URL.format(barcode=barcode))
        if response.status_code == 200:
            product_data = response.json().get('product', {})
            return Product(
                code=product_data.get('code'),
                name=product_data.get('product_name'),
                nutriments=product_data.get('nutriments')
            )
        return None