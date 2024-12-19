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
        
    def get_cardinality_by_current_next_nodes(self, next_node: "Node") -> ViewingCardinality:
        """Get the cardinality of the current node based on the next node."""
        if next_node.row < self.row:
            return ViewingCardinality.UP
        elif next_node.row > self.row:
            return ViewingCardinality.DOWN
        elif next_node.column < self.column:
            return ViewingCardinality.LEFT
        elif next_node.column > self.column:
            return ViewingCardinality.RIGHT
        raise ValueError("Next node is not adjacent to the current node.")
    
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
        self.visited_nodes: List[Node] = []
        self.unique_visited_nodes: Set[Node] = set()

    def __str__(self) -> str:
        """String representation of the guard."""
        return f"Guard({self.current_cardinality}, {self.current_node}, {self.is_on_map}, \n{self.visited_nodes})"

    def move_directionally(self, grid: List[List[Node]], starting_node: Node | None = None, starting_cardinality: ViewingCardinality | None = None) -> "Guard":
        """Move from the current node in the given direction until an obstacle is encountered."""
        self.visited_nodes.append(self.current_node)
        self.unique_visited_nodes.add(self.current_node)
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
        if starting_node and starting_cardinality:
            # If we looped back to the starting node with the same cardinality, we are in a loop, and should return self
            if self.current_node == starting_node and self.current_cardinality == starting_cardinality:
                return self
        
        return self.move_directionally(grid)

    def rotate_current_cardinality(self) -> None:
        """Rotate the current cardinal direction clockwise."""
        self.current_cardinality = ViewingCardinality(
            (self.current_cardinality.value % 4) + 1
        )
        
    def identify_possible_obstacles(self, grid: List[List[Node]]) -> Set[Node]:
        """Identify where a single obstacle could be placed in front of a guard to force them into a loop."""
        possible_obstacles: Set[Node] = set()
        
        while self.is_on_map:
            self.move_directionally(grid)
        
        original_visited_nodes = self.visited_nodes.copy()
        
        print('Finished collecting visited nodes, and will now check for possible obstacles', self.visited_nodes)
        
        for index, node in enumerate(original_visited_nodes[:-1]):
            self.visited_nodes = []
            self.unique_visited_nodes = set()
            
            self.current_node = node
            self.current_cardinality = node.get_cardinality_by_current_next_nodes(original_visited_nodes[index + 1])
            
            print('Checking if obstacle can be placed in front of the current node', node)
            # Update the next node to be an obstacle 
            original_next_node = original_visited_nodes[index + 1]
            next_node_original_value = original_next_node.value
            grid[original_next_node.row][original_next_node.column].value = NodeValue.OBSTACLE
            
            # Move the guard directionally to see if they can make it back to the starting node
            guard = self.move_directionally(grid, starting_node=node, starting_cardinality=self.current_cardinality)
            
            # If the guard is still on the map then we discovered a loop, meaning the obstacle should be added to our set
            if guard.is_on_map:
                possible_obstacles.add(original_next_node)
            
            # Revert the next node to its original value 
            grid[original_next_node.row][original_next_node.column].value = next_node_original_value
            
        return possible_obstacles
            
            
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
    
    grid = Node.input_to_grid(lines)

    starting_node = Node.get_starting_node(grid)
    guard = Guard(starting_node)
    
    result = guard.identify_possible_obstacles(grid)
    
    return len(result)


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
