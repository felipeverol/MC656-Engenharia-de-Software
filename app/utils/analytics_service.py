from . import observer
from app.database import models 

def log_new_product(product: models.Product):
    # Esta função será chamada quando o evento 'product_created' for disparado.
    print(f"--- [AnalyticsService] NOTIFICADO: Novo produto cadastrado! ---")
    print(f"    Barcode: {product.barcode}")
    print(f"    Nome: {product.name}")
    print(f"----------------------------------------------------------------")

def setup_analytics_observers():
    #Uma função para registrar todos os "ouvintes" de analytics.
    observer.subscribe("product_created", log_new_product)