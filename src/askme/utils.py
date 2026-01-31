import os

def read_file_lines(path):
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def write_file_lines(path, lines, append=True):
    mode = 'a' if append else 'w'
    with open(path, mode, encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")

def split_string(s, delimiter=','):
    return s.split(delimiter)

def input_int(prompt, low=None, high=None):
    while True:
        try:
            val = int(input(prompt))
            if (low is None or val >= low) and (high is None or val <= high):
                return val
            print(f"Enter a number in range {low}-{high}")
        except ValueError:
            print("Invalid number. Try again.")

def show_menu(choices):
    print("\nMenu:")
    for idx, choice in enumerate(choices, 1):
        print(f"\t{idx}. {choice}")
    return input_int("Choose an option: ", 1, len(choices))

def input_int(prompt, low=None, high=None):
    while True:
        try:
            value = int(input(prompt))
            if low is not None and value < low:
                print(f"Value must be at least {low}")
                continue
            if high is not None and value > high:
                print(f"Value must be at most {high}")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

