import keyboard


def get_option(msg, options_array):
    option_input = input(msg)

    if not option_input.isnumeric():
        print("Incorrect option!")
        return get_option(msg, options_array)

    option_input = int(option_input)

    if option_input < 0 or option_input >= len(options_array):
        print("Incorrect option!")
        return get_option(msg, options_array)

    return option_input


def get_key_input(exit_program=True, back_to_main=True):
    print("\n")
    if exit_program:
        print("Press SPACE to exit program.")
    if back_to_main:
        print("Press BACKSPACE to go back to main page.")
    while True:
        if keyboard.is_pressed('space') and exit_program:
            return 1
        if keyboard.is_pressed('backspace') and back_to_main:
            return 2
