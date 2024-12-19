"""Script to solve Advent of Code puzzles."""

import argparse
import os
from solutions.utils import read_input


class Antinode:
    def __init__(self, column: int, row: int):
        self.column = column
        self.row = row

    def __repr__(self):
        return f"Antinode(column={self.column}, row={self.row})"
    
    def __eq__(self, other):
        if not isinstance(other, Antinode):
            return False
        return self.column == other.column and self.row == other.row
    
    def __hash__(self):
        return hash((self.column, self.row))

class Antenna:
    def __init__(self, column: int, row: int, frequency: str):
        self.column = column
        self.row = row
        self.frequency = frequency

    def __repr__(self):
        return f"Antenna(column={self.column}, row={self.row}, frequency={self.frequency})"

def calculate_antinodes(antenna_1: Antenna, antenna_2: Antenna) -> tuple[Antinode, Antinode]:
    row_diff = antenna_1.row - antenna_2.row
    column_diff = antenna_1.column - antenna_2.column
    
    antinode_1 = Antinode(antenna_1.column, antenna_1.row)
    antinode_2 = Antinode(antenna_2.column, antenna_2.row)
    
    if row_diff > 0:
        antinode_1.row = antenna_2.row - abs(row_diff)
        antinode_2.row = antenna_1.row + abs(row_diff)
    elif row_diff < 0:
        antinode_1.row = antenna_2.row + abs(row_diff)
        antinode_2.row = antenna_1.row - abs(row_diff)
    
    if column_diff > 0:
        antinode_1.column = antenna_2.column - abs(column_diff)
        antinode_2.column = antenna_1.column + abs(column_diff)
    elif column_diff < 0:
        antinode_1.column = antenna_2.column + abs(column_diff)
        antinode_2.column = antenna_1.column - abs(column_diff)
    
    return (antinode_1, antinode_2)

def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0
    
    antennas = []
    
    for row, line in enumerate(lines):
        for column, frequency in enumerate(line):
            if frequency != '.':
                antennas.append(Antenna(column, row, frequency))
    
    antinodes = set()
    
    for i, antenna in enumerate(antennas):
        for antenna_2 in antennas[i+1:]:
            if antenna.frequency == antenna_2.frequency:
                antinode_1, antinode_2 = calculate_antinodes(antenna, antenna_2)
                antinodes.add(antinode_1)
                antinodes.add(antinode_2)
    
    row_count = len(lines)
    column_count = len(lines[0])
    
    # For each antinode whose column and row are within our grid, add 1 to the result
    for antinode in antinodes:
        if 0 <= antinode.column < column_count and 0 <= antinode.row < row_count:
            result += 1
    
    # 558 TOO HIGH
    return result

def calculate_antinodes_considering_harmonic_frequencies(antenna_1: Antenna, antenna_2: Antenna, max_rows: int, max_columns: int) -> set[Antinode]:
    row_diff = antenna_1.row - antenna_2.row
    column_diff = antenna_1.column - antenna_2.column
    antinodes = set()
    
    row = antenna_1.row
    column = antenna_1.column
    
    while 0 <= row < max_rows and 0 <= column < max_columns:
        antinodes.add(Antinode(column, row))
        row += row_diff
        column += column_diff
    
    # Add antinodes in the other direction
    row_diff = -row_diff
    column_diff = -column_diff
    
    row = antenna_1.row
    column = antenna_1.column
    
    while 0 <= row < max_rows and 0 <= column < max_columns:
        antinodes.add(Antinode(column, row))
        row += row_diff
        column += column_diff

    return antinodes


def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0
    
    antennas = []
    
    for row, line in enumerate(lines):
        for column, frequency in enumerate(line):
            if frequency != '.':
                antennas.append(Antenna(column, row, frequency))
    
    antinodes = set()
    
    row_count = len(lines)
    column_count = len(lines[0])
    
    for i, antenna in enumerate(antennas):
        for antenna_2 in antennas[i+1:]:
            if antenna.frequency == antenna_2.frequency:
                new_antinodes = calculate_antinodes_considering_harmonic_frequencies(antenna, antenna_2, row_count, column_count)
                antinodes.update(new_antinodes)
    
    # For each antinode whose column and row are within our grid, add 1 to the result
    for antinode in antinodes:
        if 0 <= antinode.column < column_count and 0 <= antinode.row < row_count:
            result += 1
    
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
