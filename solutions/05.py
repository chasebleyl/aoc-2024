"""Script to solve Advent of Code puzzles."""

import argparse
import os
from solutions.utils import read_input

class Rule:
    """A page ordering rule, defining a page number and a list of pages that must come before or after it."""
    def __init__(self, page: int, after: set[int] = set()):
        # Page number
        self.page = page
        
        # Page numbers that must come after this page
        self.after_pages = after
    
    @classmethod
    def from_str(cls, line: str) -> 'Rule':
        """Create a Rule from a string."""
        page, _, after = line.partition('|')
        return cls(int(page), {int(after)})
        
    def is_before(self, page_number: int) -> bool:
        """Check if the current rule's page number comes before another rule's page number."""
        return page_number in self.after_pages
    
    def is_before_all(self, page_numbers: list[int]) -> bool:
        """Check if the current rule's page number comes before all other rule's page numbers."""
        return all(self.is_before(page_number) for page_number in page_numbers)
    
    def is_before_any(self, page_numbers: list[int]) -> bool:
        """Check if the current rule's page number comes before any other rule's page numbers."""
        return any(self.is_before(page_number) for page_number in page_numbers)
   
class Rules:
    """A collection of rules."""
    def __init__(self, rules: dict[int, Rule] = {}):
        self.rules = rules
    
    def upsert_rule(self, rule: Rule):
        """Add a rule to the collection, or update an existing rule."""
        selected_rule = self.rules.get(rule.page)
        if selected_rule:
            selected_rule.after_pages.update(rule.after_pages)
        else:
            self.rules[rule.page] = rule
    
def parse_rules_updates(lines: list[str]) -> tuple[list[str], list[str]]:
    """Given input list of strings, split on the empty newline to return two lists of strings."""
    return lines[:lines.index('')], lines[lines.index('') + 1:]

def get_middle_number(page_numbers: list[int]) -> int:
    """Given a list of page numbers, return the middle number, irrespective of sorting."""
    return page_numbers[len(page_numbers) // 2]

def is_valid_update(rules: Rules, page_updates: list[int]) -> bool:
    """Check if a list of page updates is valid."""
    for i, page in enumerate(page_updates):
        rule = rules.rules.get(page)
        # If a rule exists, verify the rule is before all subsequent pages, and NOT before any previous pages
        if rule:
            subsequent_pages = page_updates[i+1:] if i < len(page_updates) - 1 else []
            previous_pages = page_updates[:i]
            if not rule.is_before_all(subsequent_pages) or rule.is_before_any(previous_pages):
                return False
    return True

def solve_part1(lines):
    """Solve part 1 of the puzzle."""
    result = 0
    
    raw_rules, raw_updates = parse_rules_updates(lines)
    
    rules = Rules()
    
    for rule in raw_rules:
        rules.upsert_rule(Rule.from_str(rule))
        
    for update in raw_updates:
        page_updates = [int(page) for page in update.split(',')]
        if is_valid_update(rules, page_updates):
            result += get_middle_number(page_updates)
    
    return result

def move_ints_after_index(numbers: list[int], index: int, movable_ints: list[int]) -> list[int]:
    """
    Reorders a list by moving specified integers that appear before the index to immediately after it.
    
    Args:
        numbers: List of integers to reorder
        index: Target index position
        movable_ints: List of integers that should be moved if they appear before index
        
    Returns:
        New list with movable integers repositioned after the index
    """
    # Create lists for numbers to move and numbers to keep
    to_move = []
    result = []
    
    # Collect numbers before index
    for i in range(index + 1):
        if i < len(numbers):
            if numbers[i] in movable_ints:
                to_move.append(numbers[i])
            else:
                result.append(numbers[i])
    
    # Add moved numbers after index
    result.extend(to_move)
    
    # Add remaining numbers
    if index + 1 < len(numbers):
        result.extend(numbers[index + 1:])
    
    return result


def solve_part2(lines):
    """Solve part 2 of the puzzle."""
    result = 0
    
    valid_updates = []
    invalid_updates = []
    
    raw_rules, raw_updates = parse_rules_updates(lines)
    
    rules = Rules()
    
    for rule in raw_rules:
        rules.upsert_rule(Rule.from_str(rule))
        
    for update in raw_updates:
        page_updates = [int(page) for page in update.split(',')]
        if is_valid_update(rules, page_updates):
            valid_updates.append(page_updates)
        else:
            invalid_updates.append(page_updates)

    for update in invalid_updates:
        i = 0
        while i < len(update):
            rule = rules.rules.get(update[i])
            if rule:
                # Count how many elements we'll move
                moves_count = sum(1 for x in update[:i] if x in rule.after_pages)
                new_update = move_ints_after_index(update, i, list(rule.after_pages))
                
                if is_valid_update(rules, new_update):
                    result += get_middle_number(new_update)
                    break
                else:
                    update = new_update
                    # Given we moved previous elements to after the current index,
                    # we need to adjust the index accordingly
                    i = max(0, i - moves_count)
            i += 1
    
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
