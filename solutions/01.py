"""Script to solve Advent of Code puzzles."""

import argparse
import os
from solutions.utils import read_input


def convert_lines_to_lists(lines) -> tuple[list[int], list[int]]:
    """Convert input lines to two lists of numbers."""
    return [int(line.split()[0]) for line in lines], [int(line.split()[1]) for line in lines]


def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0
    
    column_a, column_b = convert_lines_to_lists(lines)
    
    # Sort both columns
    column_a.sort()
    column_b.sort()
    
    for i, a in enumerate(column_a):
        result += abs(a - column_b[i])
    
    return result


def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0    
    
    column_a, column_b = convert_lines_to_lists(lines)
    
    # Sort both columns
    column_a.sort()
    column_b.sort()
    
    num_counts = []
      
    for num in column_a:
        num_counts.append([num, column_b.count(num)])
    
    for num, count in num_counts:
        result += num * count
    
    return result


def main():
    """Main function to solve the puzzle."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Solve Advent of Code puzzle')
    parser.add_argument('--test', action='store_true', default=False,
                       help='Run with test input instead of real input')
    args = parser.parse_args()

    # Get day number from filename
    day = int(os.path.basename(__file__).split('.')[0])

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
