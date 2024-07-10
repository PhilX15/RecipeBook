import math

import textdistance
import requests
import heapq

import input_util
import mealdb_util
import print_util


def display_main_page():
    options = ["Search by name", "Search by main ingredient", "Smart search"]

    print_util.print_text_in_box("R E C I P E\nD A T A B A S E", 20, 1)
    print_util.print_text_in_lines(
        "Welcome to Recipe Database! You can start recipe search by selecting one of the options below.", 50)
    print_util.print_list(options)

    option = input_util.get_option("Select option: ", options)
    if options[option] == "Search by name":
        search_by_name()
    elif options[option] == "Search by main ingredient":
        search_by_main_ingredient()
    else:
        smart_search()


def search_by_name():
    print_util.clear()
    name = input("Enter meal name: ")

    req = requests.get(f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}')
    database = req.json()
    req.close()

    if database['meals'] is None:
        print("Nothing found")
        if input_util.get_key_input(True, True) == 2:
            print_util.clear()
            display_main_page()
        else:
            return
        return

    meals = database['meals']
    option = 0
    if len(meals) > 0:
        print_util.clear()
        print_util.print_meals_list(meals)
        option = input_util.get_option("Select meal: ", meals)

    print_util.clear()
    print_util.print_meal_data(meals[option])
    if input_util.get_key_input(True, True) == 2:
        print_util.clear()
        display_main_page()
    else:
        return


def search_by_main_ingredient():
    print_util.clear()
    ingredient = input("Enter main ingredient: ")

    req = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}')
    database = req.json()
    req.close()

    if database['meals'] is None:
        print("Nothing found")
        if input_util.get_key_input(True, True) == 2:
            print_util.clear()
            display_main_page()
        else:
            return
        return

    meals = database['meals']
    option = 0
    if len(meals) > 0:
        print_util.clear()
        print_util.print_meals_list(meals)
        option = input_util.get_option("Select meal: ", meals)

    meal = mealdb_util.get_meal_by_id(meals[option]["idMeal"])

    print_util.clear()
    print_util.print_meal_data(meal)
    if input_util.get_key_input(True, True) == 2:
        print_util.clear()
        display_main_page()
    else:
        return


def smart_search():
    print_util.clear()
    print("Loading recipes...")
    recipes = mealdb_util.get_all_recipes()
    print("Loading ingredients...")
    ingredients = mealdb_util.get_all_ingredients()

    print_util.clear()
    print_util.print_text_in_box("SMART SEARCH")
    print_util.print_text_in_lines(
        "Want a meal that requires specific ingredients? Enter every ingredient you need for best results!")
    data = []
    while True:
        ingredient = input("Enter ingredient name: ").lower()
        if len(ingredient) == 0:
            break
        possibilities = []
        found = False
        for ing in ingredients:
            if textdistance.levenshtein(ingredient, ing) == 0:
                found = True
                break
            if textdistance.levenshtein(ingredient, ing) < 3:
                possibilities.append(ing)

        if not found and len(possibilities) == 0:
            print("Ingredient not found")
            continue

        if not found and len(possibilities) != 0:
            print_util.print_list(possibilities)
            option = input_util.get_option("Did you mean?: ", possibilities)
            ingredient = possibilities[option]

        data.append(ingredient)

    result = calculate_similarity(recipes, data)

    if max(result.values()) < 0.5:
        print("No matching meal found")
        if input_util.get_key_input(True, True) == 2:
            print_util.clear()
            display_main_page()
        else:
            return

    max_heap = [(-similarity, meal) for meal, similarity in result.items() if similarity > 0.5]
    heapq.heapify(max_heap)
    best_results = [heapq.heappop(max_heap) for _ in range(len(max_heap))]
    best_results = dict((meal, -similarity) for similarity, meal in best_results)

    result_meals = []
    for best in best_results.keys():
        req = requests.get(f'https://www.themealdb.com/api/json/v1/1/search.php?s={best}')
        meal = req.json()
        req.close()
        result_meals.append(meal['meals'][0])

    option = 0
    if len(result_meals) > 0:
        print_util.clear()
        print_util.print_list(
            [meal['strMeal'] + f' ({math.floor(best_results[meal["strMeal"]] * 100)}% similarity)' for meal in
             result_meals])
        option = input_util.get_option("Select meal: ", result_meals)

    print_util.clear()
    print_util.print_meal_data(result_meals[option])
    if input_util.get_key_input(True, True) == 2:
        print_util.clear()
        display_main_page()
    else:
        return


def calculate_similarity(meals, ingredients):
    possible_meals = {}
    for meal in meals:
        meal_ingredients = mealdb_util.get_ingredients(meal)
        similarities = 0
        for key in ingredients:
            if key in meal_ingredients.keys():
                similarities += 1

        similarity = similarities / len(meal_ingredients.keys())
        possible_meals[meal['strMeal']] = similarity

    return possible_meals


def measure_to_float(measure):
    if len(measure) == 0:
        return 0
    result = 0.0
    measure = measure.split(" ")
    try:
        result += float(measure[0])
    except:
        try:
            result += float(measure[0][0]) / float(measure[0][2])
        except:
            return 1

    if len(measure) > 1 and len(measure[1]) > 0 and measure[1][0].isnumeric():
        result += float(measure[1][0]) / float(measure[1][2])

    return result
