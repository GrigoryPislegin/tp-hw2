import pytest

from recipes import Ingredient, Recipe, ShoppingList


# Ingredient 

def test_ingredient_creation():
    ing = Ingredient("Мука", 500, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"


def test_ingredient_str():
    ing = Ingredient("Мука", 500, "г")
    assert str(ing) == "Мука: 500.0 г"


def test_ingredient_eq_same_name_and_unit():
    a = Ingredient("Мука", 500, "г")
    b = Ingredient("Мука", 200, "г")
    assert a == b


def test_ingredient_eq_different_name():
    a = Ingredient("Мука", 500, "г")
    b = Ingredient("Сахар", 500, "г")
    assert a != b


def test_ingredient_eq_different_unit():
    a = Ingredient("Молоко", 500, "мл")
    b = Ingredient("Молоко", 500, "г")
    assert a != b


# Recipe 

def test_recipe_creation():
    r = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    assert r.title == "Пицца"
    assert len(r.ingredients) == 1


def test_recipe_add_new_ingredient():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 300, "г"))
    assert len(r) == 1


def test_recipe_add_existing_ingredient_sums():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 300, "г"))
    r.add_ingredient(Ingredient("Мука", 200, "г"))
    assert len(r) == 1
    assert r.ingredients[0].quantity == 500.0


def test_recipe_scale_returns_new_object():
    r = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    scaled = r.scale(2)
    assert scaled is not r
    assert r.ingredients[0].quantity == 300.0


def test_recipe_scale_multiplies_quantity():
    r = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    scaled = r.scale(3)
    assert scaled.ingredients[0].quantity == 900.0


def test_recipe_scale_invalid_ratio():
    r = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    with pytest.raises(ValueError):
        r.scale(0)


def test_recipe_len():
    r = Recipe("Пицца")
    r.add_ingredient(Ingredient("Мука", 300, "г"))
    r.add_ingredient(Ingredient("Сыр", 150, "г"))
    assert len(r) == 2


# ShoppingList

def test_shopping_add_recipe():
    sl = ShoppingList()
    sl.add_recipe(Recipe("Пицца", [Ingredient("Мука", 300, "г")]), 2)
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].quantity == 600.0


def test_shopping_add_recipe_invalid_portions():
    sl = ShoppingList()
    r = Recipe("Пицца", [Ingredient("Мука", 300, "г")])
    with pytest.raises(ValueError):
        sl.add_recipe(r, 0)


def test_shopping_remove_recipe():
    sl = ShoppingList()
    sl.add_recipe(Recipe("Пицца", [Ingredient("Мука", 300, "г")]), 1)
    sl.add_recipe(Recipe("Салат", [Ingredient("Помидор", 2, "шт")]), 1)
    sl.remove_recipe("Пицца")
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].name == "Помидор"


def test_shopping_remove_nonexistent_recipe():
    sl = ShoppingList()
    sl.add_recipe(Recipe("Пицца", [Ingredient("Мука", 300, "г")]), 1)
    sl.remove_recipe("Несуществующий рецепт")
    assert len(sl.get_list()) == 1


def test_shopping_get_list_sums_same_ingredient():
    sl = ShoppingList()
    sl.add_recipe(Recipe("Маргарита", [Ingredient("Мука", 300, "г")]), 1)
    sl.add_recipe(Recipe("4 сыра", [Ingredient("Мука", 200, "г")]), 1)
    result = sl.get_list()
    assert len(result) == 1
    assert result[0].quantity == 500.0


def test_shopping_get_list_sorted_by_name():
    sl = ShoppingList()
    sl.add_recipe(Recipe("Блюдо", [
        Ingredient("Яблоко", 1, "шт"),
        Ingredient("Банан", 2, "шт"),
        Ingredient("Апельсин", 3, "шт"),
    ]), 1)
    names = [ing.name for ing in sl.get_list()]
    assert names == sorted(names)


def test_shopping_add_combines_lists():
    a = ShoppingList()
    a.add_recipe(Recipe("Пицца", [Ingredient("Мука", 300, "г")]), 1)
    b = ShoppingList()
    b.add_recipe(Recipe("Хлеб", [Ingredient("Мука", 200, "г")]), 1)
    combined = a + b
    result = combined.get_list()
    assert len(result) == 1
    assert result[0].quantity == 500.0


def test_shopping_add_does_not_change_originals():
    a = ShoppingList()
    a.add_recipe(Recipe("Пицца", [Ingredient("Мука", 300, "г")]), 1)
    b = ShoppingList()
    b.add_recipe(Recipe("Хлеб", [Ingredient("Мука", 200, "г")]), 1)
    _ = a + b
    assert len(a.get_list()) == 1
    assert len(b.get_list()) == 1
