def read_input(day, test=False):
    """Read the input file for a specific day and return a list of strings, one per line."""
    file_name = "test.txt" if test else "input.txt"
    file_path = f"inputs/{day:02d}/{file_name}"

    with open(file_path, 'r') as file:
        return [line.strip() for line in file]
