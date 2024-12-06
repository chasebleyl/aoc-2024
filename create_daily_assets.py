"""Script to set up a new day for Advent of Code."""

import argparse
import os
import shutil

def pad_day(day: int) -> str:
    """Convert day number to zero-padded string."""
    return str(day).zfill(2)

def setup_day(day: int):
    """Set up directory structure and files for given day."""
    day_str = pad_day(day)
    
    # Create inputs directory if it doesn't exist
    input_dir = os.path.join('inputs', day_str)
    os.makedirs(input_dir, exist_ok=True)
    
    # Create empty input files
    input_files = ['input.txt', 'test.txt']
    for file in input_files:
        input_path = os.path.join(input_dir, file)
        if not os.path.exists(input_path):
            with open(input_path, 'w', encoding='utf-8') as _:
                pass  # Create empty file
    
    # Copy solution template
    solution_template = os.path.join('solutions', '00.py')
    new_solution = os.path.join('solutions', f'{day_str}.py')
    
    if not os.path.exists(new_solution):
        if os.path.exists(solution_template):
            shutil.copy2(solution_template, new_solution)
        else:
            print(f"Warning: Template file {solution_template} not found")

def main():
    """Main function to set up a new day for Advent of Code."""
    parser = argparse.ArgumentParser(description='Set up new day for Advent of Code')
    parser.add_argument('--day', type=int, required=True, help='Day number to set up')
    
    args = parser.parse_args()
    
    if args.day < 1 or args.day > 25:
        print("Day must be between 1 and 25")
        return
    
    setup_day(args.day)
    print(f"Set up completed for day {pad_day(args.day)}")

if __name__ == "__main__":
    main()
