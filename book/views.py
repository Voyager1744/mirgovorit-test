from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Product, Recipe, ProductRecipe


@require_http_methods(["GET"])
@transaction.atomic
def add_product_to_recipe(request):
    try:
        recipe_id = request.GET.get("recipe_id")
        product_id = request.GET.get("product_id")
        weight = request.GET.get("weight")

        if not recipe_id or not product_id or not weight:
            return JsonResponse(
                {"error": "Не указаны все необходимые аргументы"}, status=400
            )

        recipe = Recipe.objects.get(id=recipe_id)
        product = Product.objects.get(id=product_id)

        weight = int(weight)

        recipe_product, _ = ProductRecipe.objects.get_or_create(
            recipe=recipe, product=product
        )
        recipe_product.weight += weight
        recipe_product.save()

    except (Recipe.DoesNotExist, Product.DoesNotExist):
        return JsonResponse({"error": "Рецепт или продукт не существует"}, status=404)
    except ValueError:
        return JsonResponse({"error": "Вес должен быть числом"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(
        {"message": "Продукт успешно добавлен/обновлен в рецепте"}, status=200
    )


@require_http_methods(["GET"])
@transaction.atomic
def cook_recipe(request):
    try:
        recipe_id = request.GET.get("recipe_id")

        if not recipe_id:
            return JsonResponse({"error": "Не указан рецепт"}, status=400)

        recipe = Recipe.objects.select_for_update().get(id=recipe_id)

        products_in_recipe = ProductRecipe.objects.select_related("product").filter(
            recipe=recipe
        )
        if not products_in_recipe:
            return JsonResponse({"error": "Рецепт пуст"}, status=400)

        for product_recipe in products_in_recipe:
            product = product_recipe.product
            product.count_cooks += 1
            product.save()

    except Recipe.DoesNotExist:
        return JsonResponse({"error": "Recipe does not exist"}, status=404)

    return JsonResponse({"message": "Рецепт приготовлен"}, status=200)


@require_http_methods(["GET"])
def show_recipes_without_product(request):
    product_id = request.GET.get("product_id")
    recipes = Recipe.objects.exclude(products__id=product_id).distinct()

    return render(request, "recipes.html", {"recipes": recipes})
