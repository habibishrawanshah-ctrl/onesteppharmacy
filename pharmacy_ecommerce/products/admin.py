from django.contrib import admin
from django.utils.html import format_html
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Product, Category, Wishlist, StockNotification
import csv, io

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'expiry_date', 'created_at', 'image_tag')
    readonly_fields = ('image_tag',)
    fields = ('category', 'name', 'description', 'price', 'stock', 'expiry_date', 'image', 'image_tag', 'is_prescription_required', 'manufacturer')
    search_fields = ('name', 'manufacturer')
    list_filter = ('category', 'expiry_date', 'is_prescription_required')

    def image_tag(self, obj):
        if obj.image and obj.image.name:
            return format_html('<img src="{}" style="max-height:100px; max-width:120px;" />', obj.image.url)
        return '-'

    image_tag.short_description = 'Image Preview'

    actions = ['export_csv', 'import_csv']

    def export_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'name', 'description', 'price', 'stock', 'category', 'manufacturer', 'is_prescription_required'])
        for p in queryset:
            writer.writerow([p.id, p.name, p.description, p.price, p.stock, p.category.name if p.category else '', p.manufacturer, p.is_prescription_required])
        return response
    export_csv.short_description = 'Export selected as CSV'

    def import_csv(self, request):
        if request.method == 'POST' and request.FILES.get('csv_file'):
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                self.message_user(request, 'Please upload a .csv file.', level='ERROR')
                return HttpResponseRedirect(request.path)
            decoded = csv_file.read().decode('utf-8')
            reader = csv.DictReader(io.StringIO(decoded))
            imported = 0
            errors = []
            for row in reader:
                try:
                    category = None
                    if row.get('category'):
                        category, _ = Category.objects.get_or_create(name=row['category'])
                    Product.objects.create(
                        name=row.get('name', '').strip(),
                        description=row.get('description', ''),
                        price=float(row.get('price', 0)),
                        stock=int(row.get('stock', 0)),
                        manufacturer=row.get('manufacturer', ''),
                        is_prescription_required=row.get('is_prescription_required', '').lower() in ('true', '1', 'yes'),
                        category=category,
                    )
                    imported += 1
                except Exception as e:
                    errors.append(f"Row {imported + 1}: {e}")
            msg = f'Imported {imported} products.'
            if errors:
                msg += ' Errors: ' + '; '.join(errors[:5])
            self.message_user(request, msg)
            return HttpResponseRedirect(request.path)
        return render(request, 'admin/import_csv.html')
    import_csv.short_description = 'Import products from CSV'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom = [
            path('import-csv/', self.import_csv, name='product_import_csv'),
        ]
        return custom + urls


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('user__username', 'product__name')


@admin.register(StockNotification)
class StockNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'email', 'notified', 'created_at')
    list_filter = ('notified',)
