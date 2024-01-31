import json
from django.test import TestCase
from django.test import RequestFactory
from django.urls import reverse
from .models import Recipe, Product, ProductRecipe
from .views import cook_recipe


class AddProductToRecipeTestCase(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(name="Test Recipe")
        self.product = Product.objects.create(name="Test Product")
        self.url = reverse("add_product_to_recipe")

    def test_missing_arguments(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content),
            {"error": "Не указаны все необходимые аргументы"},
        )

    def test_invalid_recipe_id(self):
        response = self.client.get(
            self.url, {"recipe_id": 999, "product_id": self.product.id, "weight": 100}
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            json.loads(response.content), {"error": "Recipe does not exist"}
        )

    def test_invalid_product_id(self):
        response = self.client.get(
            self.url, {"recipe_id": self.recipe.id, "product_id": 999, "weight": 100}
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            json.loads(response.content), {"error": "Product does not exist"}
        )

    def test_invalid_weight(self):
        response = self.client.get(
            self.url,
            {
                "recipe_id": self.recipe.id,
                "product_id": self.product.id,
                "weight": "abc",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"error": "Вес должен быть числом"}
        )

    def test_recipe_product_exists(self):
        ProductRecipe.objects.create(
            recipe=self.recipe, product=self.product, weight=100
        )
        response = self.client.get(
            self.url,
            {"recipe_id": self.recipe.id, "product_id": self.product.id, "weight": 200},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"message": "Product added/updated successfully"},
        )
        recipe_product = ProductRecipe.objects.get(
            recipe=self.recipe, product=self.product
        )
        self.assertEqual(recipe_product.weight, 300)


class CookRecipeTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.recipe = Recipe.objects.create(id=1, name="Test Recipe")
        self.product = Product.objects.create(id=1, name="Test Product")

    def test_cook_recipe_success(self):
        ProductRecipe.objects.create(
            recipe=self.recipe, product=self.product, weight=100
        )
        request = self.factory.get("/cook_recipe", {"recipe_id": 1}, {"weight": 100})
        response = cook_recipe(request)

        new_cook_count = self.product.count_cooks + 1

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_cook_count, 1)
        self.assertEqual(
            json.loads(response.content), {"message": "Рецепт приготовлен"}
        )

    def test_cook_recipe_missing_recipe_id(self):
        request = self.factory.get("/cook_recipe")
        response = cook_recipe(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"error": "Не указан рецепт"})

    def test_cook_recipe_empty_recipe(self):
        recipe = Recipe.objects.create()
        request = self.factory.get("/cook_recipe", {"recipe_id": recipe.id})
        response = cook_recipe(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content), {"error": "Рецепт пуст"})

    def test_cook_recipe_nonexistent_recipe(self):
        request = self.factory.get("/cook_recipe", {"recipe_id": 999})
        response = cook_recipe(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content), {"error": "Recipe does not exist"}
        )
