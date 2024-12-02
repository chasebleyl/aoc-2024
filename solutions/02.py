"""Script to solve Advent of Code puzzles."""

import argparse
import os
from solutions.utils import read_input

def determine_report_safety(report: list[int]) -> bool:
    """Determine if a report is safe."""
    is_safe = True
    abs_diff_min = 1
    abs_diff_max = 3
    is_ascending = None
    is_descending = None
    
    for i, num in enumerate(report):
        if i == len(report) - 1:
            break
        
        if num > report[i+1]:
            is_ascending = False
        elif num < report[i+1]:
            is_descending = False
        if is_ascending is not None and is_ascending == is_descending:
            is_safe = False
            break
        
        diff = abs(num - report[i+1])
        if diff < abs_diff_min or diff > abs_diff_max:
            is_safe = False
            break
        if is_ascending and num > report[i+1]:
            is_safe = False
            break
        if is_descending and num < report[i+1]:
            is_safe = False
            break
    return is_safe

def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0
    
    for line in lines:
        report = [int(num) for num in line.split()]
        if determine_report_safety(report):
            result += 1
    
    return result


def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0
    
    def generate_sub_reports(report: list[int]) -> list[list[int]]:
        """Generate all possible sub-reports by removing just one number from the report."""
        sub_reports = []
        for i in range(len(report)):
            sub_reports.append(report[:i] + report[i+1:])
        return sub_reports
    
    for line in lines:
        report = [int(num) for num in line.split()]
        if determine_report_safety(report):
            result += 1
        else:
            # Since the full report is not safe, generate all possible sub-reports by removing just one number from the report:
            sub_reports = generate_sub_reports(report)
            for sub_report in sub_reports:
                # Check if any of those sub-reports are safe:
                if determine_report_safety(sub_report):
                    result += 1
                    break
    
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
