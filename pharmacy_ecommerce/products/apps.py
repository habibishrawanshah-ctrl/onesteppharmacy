from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'products'
    verbose_name = 'Products'

    def ready(self):
        try:
            from django.contrib import admin
            admin.site.site_header = "ONE STEP PHARMACY"
            admin.site.site_title = "ONE STEP PHARMACY Admin"
            admin.site.index_title = "ONE STEP PHARMACY Administration"
        except Exception:
            pass
