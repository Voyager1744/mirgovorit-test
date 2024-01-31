from django.contrib import admin

from .models import Product, Recipe, ProductRecipe


class ProductRecipeInline(admin.TabularInline):
    model = ProductRecipe
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    inlines = (ProductRecipeInline,)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "count_cooks")
    ordering = ("-count_cooks",)
    search_fields = ("name",)


@admin.register(ProductRecipe)
class ProductRecipeAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "recipe", "weight")
    ordering = ("-weight",)
    search_fields = ("product__name", "recipe__name")
