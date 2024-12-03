"""Script to solve Advent of Code puzzles."""

import argparse
import os
import re
from solutions.utils import read_input

def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0
    
    text = "".join(lines).replace('\n',' ')
    result += sum(int(x)*int(y) for x,y in re.findall(r'mul\((\d+),(\d+)\)', text))
    
    return result


def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0
    
    text = "do()" + "".join(lines).replace('\n',' ') + "don't()"
    enabled_text = "".join(re.findall(r"do\(\)(.*?)don't\(\)", text))
    result += sum(int(x)*int(y) for x,y in re.findall(r'mul\((\d+),(\d+)\)', enabled_text))
    
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
