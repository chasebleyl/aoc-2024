"""Script to solve Advent of Code puzzles."""

import argparse
from enum import Enum
import os
from solutions.utils import read_input

class Equation:
    """Simple representation of the components of an equation, minus the operators."""
    def __init__(self, equation: str, result: int, variables: list[int]):
        self.equation = equation
        self.result = result
        self.variables = variables
        
    @staticmethod
    def from_line(line: str) -> "Equation":
        """Create an Equation from a string line of input."""
        result, equation = line.split(':')
        variables = [int(variable) for variable in equation.split()]
        return Equation(line, int(result), variables)
    
class Operations(Enum):
    """Simple representation of the operations that can be performed on an equation."""
    ADD = '+'
    MULTIPLY = '*'
    
def resolove_inputs_with_operations(input_a: int, input_b: int, operation: Operations) -> int:
    """Resolve the inputs with the operation."""
    if operation == Operations.ADD:
        return input_a + input_b
    elif operation == Operations.MULTIPLY:
        return input_a * input_b
    else:
        raise ValueError(f"Unknown operation: {operation}")

def try_operations(variables: list[int], target: int, current_value: int = None, index: int = 0) -> list[Operations] | None:
    """
    Recursively try different operations to reach the target value.
    Returns list of operations if solution found, None otherwise.
    """
    # Base case: if we've used all variables except the last one
    if index == len(variables) - 1:
        if current_value is None:
            return [] if variables[0] == target else None
        return [] if current_value == target else None
    
    # Initialize current_value with first number if not set
    if current_value is None:
        current_value = variables[0]
        index = 1
    
    # Try each operation
    for operation in Operations:
        print("Attempting iteration of operation", operation)
        next_value = resolove_inputs_with_operations(current_value, variables[index], operation)
        result = try_operations(variables, target, next_value, index + 1)
        if result is not None:
            return [operation] + result
            
    return None

def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0
    equations = [Equation.from_line(line) for line in lines]
    
    for equation in equations:
        print("Attempting to solve equation", equation.equation)
        operations = try_operations(equation.variables, equation.result)
        if operations is not None:
            result += 1
            # Print the solution for debugging
            print(f"Solution found: {' '.join([str(v) + ' ' + op.value for v, op in zip(equation.variables[:-1], operations)])} {equation.variables[-1]} = {equation.result}")
        else:
            print(f"No solution found for equation {equation.equation}")
    
    return result


def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0
    # Your part 2 solution code here
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
