import math
import os


def print_text_in_box(msg, side_margin=2, margin=0):
    lines = msg.split("\n")
    width = max(len(line) for line in lines) + (side_margin * 2)
    box = f'+{"-" * width}+\n'
    empty_line = f'|{" " * width}|\n'
    box += f'{empty_line * margin}'
    for line in lines:
        margin_left = width - len(line)
        margin_right = math.ceil(margin_left / 2)
        margin_left //= 2
        box += f'|{" " * margin_left}{line}{" " * (margin_right)}|\n'
    box += f'{empty_line * margin}'
    box += f'+{"-" * width}+\n'
    print(box)


def print_text_in_half_box(msg, side_margin=2, margin=0):
    lines = msg.split("\n")
    width = max(len(line) for line in lines) + (side_margin * 2)
    half_box = f'{"-" * width}\n'
    empty_line = f'{" " * width}\n'
    half_box += f'{empty_line * margin}'
    for line in lines:
        margin_left = width - len(line)
        margin_right = math.ceil(margin_left / 2)
        margin_left //= 2
        half_box += f'{" " * margin_left}{line}{" " * (margin_right)}\n'
    half_box += f'{empty_line * margin}'
    half_box += f'{"-" * width}\n'
    print(half_box)


def print_text_in_lines(msg, min_line_length=50):
    first_char = 0
    while first_char < len(msg):
        line_length = min_line_length
        while first_char + line_length < len(msg) and (msg[first_char + line_length] != ' '):
            line_length += 1
        if msg[first_char] == ' ':
            first_char += 1
        print(msg[first_char:first_char + line_length])
        first_char += line_length
    print()


def print_list(list_to_print, paragraph_format="[]"):
    for i in range(len(list_to_print)):
        print(f"{paragraph_format[0]}{i}{paragraph_format[1]} {list_to_print[i]}")
    print()


def print_meal_data(meal, name=True, instructions=True, ingredients=True, measures=True):
    if name:
        print_text_in_box(meal['strMeal'].upper() + "\nRECIPE")
    if instructions:
        print_text_in_half_box("INSTRUCTIONS")
        for line in meal['strInstructions'].replace("\r\n\r\n", "\n").split("\n"):
            print_text_in_lines(line)
            print()
    if ingredients:
        print_text_in_half_box("INGREDIENTS")
        for i in range(1, 21):
            ingredient = f'strIngredient{i}'
            if meal[ingredient] is None or len(meal[ingredient]) == 0:
                break
            print(f'- {meal[ingredient]}', end="")
            measure = f'strMeasure{i}'
            if measures and len(measure) > 0:
                print(f' ({meal[measure]})')
            else:
                print()


def print_meals_list(meals):
    for i in range(len(meals)):
        print(f'[{i}] {meals[i]["strMeal"]}')


def clear():
    os.system('cls') if os.name == 'nt' else os.system('clear')
