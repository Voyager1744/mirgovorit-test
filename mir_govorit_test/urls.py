from django.contrib import admin
from django.urls import path, include


funcs = [
    # path('add_product_to_recipe', add_product_to_recipe, name='add_product_to_recipe'),
    # path('cook_recipe', cook_recipe, name='cook_recipe'),
    # path('show_recipes_without_product', show_recipes_without_product, name='show_recipes_without_product'),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(funcs)),
]
