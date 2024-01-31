from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    name = models.CharField(max_length=100)
    count_cooks = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} (id={self.id})"


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(
        Product, through="ProductRecipe", related_name="recipes"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name


class ProductRecipe(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    weight = models.IntegerField(
        "Вес в г", validators=[MinValueValidator(1, "Минимальный вес 1 гр.")]
    )

    class Meta:
        ordering = ["-weight"]
        unique_together = ["product", "recipe"]
        verbose_name = "Продукт в рецепте"
        verbose_name_plural = "Продукты в рецептах"

    def __str__(self):
        return f"{self.product.name} {self.weight} г."
