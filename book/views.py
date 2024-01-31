from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Product, Recipe, ProductRecipe


@require_http_methods(["GET"])
def add_product_to_recipe(request):
    try:
        recipe_id = request.GET.get("recipe_id")
        product_id = request.GET.get("product_id")
        weight = request.GET.get("weight")

        if not recipe_id or not product_id or not weight:
            return JsonResponse({"error": "Не указаны все необходимые аргументы"}, status=400)

        recipe = Recipe.objects.get(id=recipe_id)
        if not recipe:
            return JsonResponse({"error": "Рецепт не найден"}, status=404)

        product = Product.objects.get(id=product_id)
        if not product:
            return JsonResponse({"error": "Продукт не найден"}, status=404)

        try:
            weight = int(weight)
        except ValueError:
            return JsonResponse({"error": "Вес должен быть числом"}, status=400)

        recipe_product = ProductRecipe.objects.filter(recipe=recipe, product=product).first()
        if recipe_product:
            recipe_product.weight += int(weight)
            recipe_product.save()
        else:
            ProductRecipe.objects.create(recipe=recipe, product=product, weight=int(weight))

    except Recipe.DoesNotExist:
        return JsonResponse({"error": 'Recipe does not exist'}, status=500)
    except Product.DoesNotExist:
        return JsonResponse({"error": 'Product does not exist'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'message': 'Product added/updated successfully'}, status=200)


@require_http_methods(["GET"])
def cook_recipe(request):
    try:
        recipe_id = request.GET.get("recipe_id")

        if not recipe_id:
            return JsonResponse({"error": "Не указан рецепт"}, status=400)

        recipe = Recipe.objects.get(id=recipe_id)
        if not recipe:
            return JsonResponse({"error": "Рецепт не найден"}, status=404)

        products_in_recipe = ProductRecipe.objects.filter(recipe=recipe)
        if not products_in_recipe:
            return JsonResponse({"error": "Рецепт пуст"}, status=400)

        for product in products_in_recipe:
            product.product.count_cooks += 1
            product.product.save()

    except Recipe.DoesNotExist:
        return JsonResponse({"error": 'Recipe does not exist'}, status=500)

    return JsonResponse({'message': 'Рецепт приготовлен'}, status=200)


@require_http_methods(["GET"])
def show_recipes_without_product(request):
    product_id = request.GET.get("product_id")
    recipes = Recipe.objects.exclude(products__id=product_id).distinct()

    return render(request, "recipes.html", {"recipes": recipes})


