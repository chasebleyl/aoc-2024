"""Script to solve Advent of Code puzzles."""

import argparse
import os
from enum import Enum
from typing import List, Set, Tuple
from solutions.utils import read_input


class NodeValue(Enum):
    """Enum for the values of the nodes."""

    GUARD = "^"
    OBSTACLE = "#"
    OTHER = "."


class ViewingCardinality(Enum):
    """Enum for the cardinalities of the viewing angles."""

    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Node:
    """Class to represent a node in the grid."""

    def __init__(self, row: int, column: int, value: NodeValue):
        # Coordinate traveling west and east
        self.row = row
        # Coordinate traveling north and south
        self.column = column
        self.value = value
        
    def __str__(self) -> str:
        """String representation of the node."""
        return f"Node({self.row}, {self.column}, {self.value.value})"

    def __repr__(self) -> str:
        """Representation of the node."""
        return self.__str__()

    def get_next_node(
        self, grid: List[List["Node"]], direction: ViewingCardinality
    ) -> "Node":
        """Get the next node in the given direction."""
        if direction == ViewingCardinality.UP:
            return grid[self.row - 1][self.column]
        elif direction == ViewingCardinality.RIGHT:
            return grid[self.row][self.column + 1]
        elif direction == ViewingCardinality.DOWN:
            return grid[self.row + 1][self.column]
        elif direction == ViewingCardinality.LEFT:
            return grid[self.row][self.column - 1]

    def get_next_node_coordinates(
        self, direction: ViewingCardinality
    ) -> Tuple[int, int]:
        """Get the coordinates of the next node without checking if it's in the grid."""
        if direction == ViewingCardinality.UP:
            return self.row - 1, self.column
        elif direction == ViewingCardinality.RIGHT:
            return self.row, self.column + 1
        elif direction == ViewingCardinality.DOWN:
            return self.row + 1, self.column
        elif direction == ViewingCardinality.LEFT:
            return self.row, self.column - 1

    @classmethod
    def get_starting_node(cls, grid: List[List["Node"]]) -> "Node":
        """Get the starting node from the grid."""
        for row in grid:
            for node in row:
                if node.value == NodeValue.GUARD:
                    return node
        raise ValueError("No starting node found in the grid.")

    @classmethod
    def input_to_grid(cls, lines: List[str]) -> List[List["Node"]]:
        """Convert the input lines to a grid of nodes."""
        return [
            [Node(x, y, NodeValue(value)) for y, value in enumerate(line)]
            for x, line in enumerate(lines)
        ]


class Guard:
    """Class to represent a guard."""

    def __init__(self, starting_node: Node):
        self.current_cardinality = ViewingCardinality.UP
        self.current_node = starting_node
        self.is_on_map = True
        self.visited_nodes: Set[Node] = set()

    def __str__(self) -> str:
        """String representation of the guard."""
        return f"Guard({self.current_cardinality}, {self.current_node}, {self.is_on_map}, \n{self.visited_nodes})"

    def move_directionally(self, grid: List[List[Node]]) -> "Guard":
        """Move from the current node in the given direction until an obstacle is encountered."""
        self.visited_nodes.add(self.current_node)
        # If the next node is not in the grid, update is on map and return
        next_node_coordinates = self.current_node.get_next_node_coordinates(
            self.current_cardinality
        )
        if not 0 <= next_node_coordinates[0] < len(
            grid
        ) or not 0 <= next_node_coordinates[1] < len(grid[0]):
            self.is_on_map = False
            return self
        next_node = self.current_node.get_next_node(grid, self.current_cardinality)
        # If we encounter an obstacle, rotate cardinality and return
        if grid[next_node.row][next_node.column].value == NodeValue.OBSTACLE:
            self.rotate_current_cardinality()
            return self
        # Otherwise, keep moving
        self.current_node = next_node
        return self.move_directionally(grid)

    def rotate_current_cardinality(self) -> None:
        """Rotate the current cardinal direction clockwise."""
        self.current_cardinality = ViewingCardinality(
            (self.current_cardinality.value % 4) + 1
        )

    @property
    def visited_nodes_count(self) -> int:
        """Get the number of unique visited nodes."""
        return len(self.visited_nodes)


def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0

    grid = Node.input_to_grid(lines)

    starting_node = Node.get_starting_node(grid)
    guard = Guard(starting_node)

    while guard.is_on_map:
        guard.move_directionally(grid)

    result = guard.visited_nodes_count

    return result


def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0
    # Your part 2 solution code here
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
