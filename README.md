Небольшая библиотека на Python для работы с рецептами: описание ингредиентов,
объединение их в рецепты, масштабирование порций и формирование общего списка
покупок для нескольких рецептов сразу.

Реализованные классы (`recipes.py`):

`Ingredient` — продукт с названием, количеством и единицей измерения;
`Recipe` — рецепт блюда с набором ингредиентов и масштабированием порций;
`DietaryRecipe` — рецепт с диетической категорией (веган, без глютена и т.д.);
`ShoppingList` — список покупок, который суммирует одинаковые продукты из разных рецептов.

Установка 

```bash
git clone https://github.com/GrigoryPislegin/tp-hw2.git
cd tp-hw2
pip install -r requirements.txt
```

Использование 

Пример работы с классами:

```python
from recipes import Ingredient, Recipe, ShoppingList

margarita = Recipe("Маргарита", [
    Ingredient("Мука", 300, "г"),
    Ingredient("Сыр", 150, "г"),
])

shopping = ShoppingList()
shopping.add_recipe(margarita, portions=2)

for ingredient in shopping.get_list():
    print(ingredient)
```

Запуск тестов:

```bash
pytest
```

Автор

Пислегин Григорий Викторович, группа БУЦП251
