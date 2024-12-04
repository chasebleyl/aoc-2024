"""Script to solve Advent of Code puzzles."""

import argparse
import os
import numpy as np
from solutions.utils import read_input


def get_diagonals(matrix):
    """Get all possible diagonals from a matrix (both directions)."""
    rows, cols = matrix.shape
    diagonals = []

    # Get all diagonals (top-left to bottom-right)
    for offset in range(-(rows - 1), cols):
        diagonal = np.diagonal(matrix, offset=offset)
        if len(diagonal) >= 4:  # Only include diagonals that could contain "XMAS"
            diagonals.append("".join(diagonal))

    # Flip matrix horizontally to get diagonals in other direction
    flipped_matrix = np.fliplr(matrix)
    for offset in range(-(rows - 1), cols):
        diagonal = np.diagonal(flipped_matrix, offset=offset)
        if len(diagonal) >= 4:  # Only include diagonals that could contain "XMAS"
            diagonals.append("".join(diagonal))

    return diagonals


def count_xmas(line) -> int:
    """Count instances of "XMAS" or "SAMX" in string line."""
    return line.count("XMAS") + line.count("SAMX")


def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0

    # Convert input to numpy array
    matrix = np.array([list(line) for line in lines])

    # Check rows (each row is already a string)
    for row in lines:
        result += count_xmas(row)

    # Check columns
    for col in range(matrix.shape[1]):
        column_str = "".join(matrix[:, col])
        result += count_xmas(column_str)

    # Check all possible diagonals
    for diagonal in get_diagonals(matrix):
        result += count_xmas(diagonal)

    return result

def is_mas_x_window(window):
    """Check if a 3x3 window makes an X our of MAS, with A in the middle and MAS spelled diagonally both ways."""    
    def check_mas_x(matrix):
        # check if the middle of the matrix is A
        if matrix[1, 1] != "A":
            return False
        
        # Retrieve the two diagonals from the four corners
        mas_comparator = np.array(["M", "A", "S"])
        sam_comparator = np.array(["S", "A", "M"])
        
        # If the first diagonal is not MAS or SAM, return False
        top_left_diagonal = np.array([matrix[0, 0], matrix[1, 1], matrix[2, 2]])
        if not np.array_equal(top_left_diagonal, mas_comparator) and not np.array_equal(top_left_diagonal, sam_comparator):
            return False
        
        # If the second diagonal is not MAS or SAM, return False
        bottom_left_diagonal = np.array([matrix[0, 2], matrix[1, 1], matrix[2, 0]])
        if not np.array_equal(bottom_left_diagonal, mas_comparator) and not np.array_equal(bottom_left_diagonal, sam_comparator):
            return False
        
        # If both diagonals are MAS or SAM, return True
        return True
    
    if check_mas_x(window):
        return True
    
    return False

def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0
    
    # Convert list of strings to numpy array
    matrix = np.array([list(line) for line in lines])
    
    # Iterate through matrix in 3x3 windows
    for i in range(len(lines) - 2):
        for j in range(len(lines[0]) - 2):
            window = matrix[i:i+3, j:j+3]
            if is_mas_x_window(window):
                result += 1
    
    return result


def main():
    """Main function to solve the puzzle."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Solve Advent of Code puzzle")
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="Run with test input instead of real input",
    )
    args = parser.parse_args()

    # Get day number from filename
    day = int(os.path.basename(__file__).split(".")[0])

    # Read input
    lines = read_input(day, test=args.test)

    # Solve part 1
    part1_result = solve_part1(lines)
    print(f"Part 1: {part1_result}")

    # Solve part 2
    part2_result = solve_part2(lines)
    print(f"Part 2: {part2_result}")


if __name__ == "__main__":
    main()
