# HW3 Sudoku CSP Solver — Starter Guide

This directory contains the starter code for the Sudoku solver you will build in HW3. You will implement a Constraint Satisfaction Problem (CSP) solver using backtracking search with optional heuristics and inference techniques to efficiently solve Sudoku puzzles.

## What is a CSP?

A Constraint Satisfaction Problem consists of:
- **Variables**: The 81 cells in a 9x9 Sudoku grid
- **Domains**: Possible values (1-9) for each cell
- **Constraints**: No duplicate values in any row, column, or 3x3 box

Your solver will use backtracking search to assign values to variables while respecting these constraints.

## Repository Layout

- `main.py` – Entry point that launches the Tkinter UI (`sudoku.app.main`).
- `sudoku/csp.py` – **Where you will implement `solve`**. The file currently raises `NotImplementedError`.
- `sudoku/app.py` – GUI application with 59 test puzzles and solver options; calls your `solve` implementation.
- `requirements.txt` – Python dependencies (Tkinter and pytest).

## Getting Started

1. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

2. Install dependencies from the starter directory:
   ```bash
   pip install -r requirements.txt
   ```
   Tkinter is included with most Python installations.

3. Run the GUI to test your implementation:
   ```bash
   python main.py
   ```

## Running the Application

Launch the GUI with:
```bash
python main.py
```

**Features:**
- Load random puzzles using the "New" button or select from 59 built-in puzzles
- Manually play by clicking cells and typing digits (1-9)
- Use Shift+digit to add pencil marks (notes) for solving strategies
- Click "Solve (AI)" to run your CSP solver
- Toggle solver optimizations (MRV, LCV, Forward Checking, AC-3) using checkboxes
- "Auto Notes" fills in possible candidates for empty cells
- "Validate" checks for constraint violations
- "Reset" returns to the original puzzle state

**Keyboard shortcuts:**
- Arrow keys or HJKL/WASD: Navigate cells
- 1-9: Enter value
- Shift+1-9: Add/remove pencil mark
- N: Toggle note mode
- V: Validate puzzle
- S: Solve with AI
- Backspace/Delete: Clear cell

## Implementing the `solve` Function

Your main task is to complete `sudoku/csp.py::solve` so it returns a solved Sudoku grid or `None` if no solution exists.

### Function Signature

```python
def solve(
    grid: Grid,
    *,
    use_mrv: bool = False,
    use_lcv: bool = False,
    use_fc: bool = False,
    use_ac3: bool = False,
) -> Optional[Grid]:
```

**Parameters:**
- `grid`: 9x9 list of lists containing strings '0'-'9' (where '0' represents an empty cell)
- `use_mrv`: Enable Minimum Remaining Values heuristic for variable selection
- `use_lcv`: Enable Least Constraining Value heuristic for value ordering
- `use_fc`: Enable Forward Checking for inference
- `use_ac3`: Enable AC-3 algorithm for preprocessing and inference

**Return:**
- A 9x9 list of lists with strings '1'-'9' representing the solved puzzle
- `None` if the puzzle has no solution

### Required Components

Your implementation should include:

1. **Domain Management**
   - Initialize domains for each cell (fixed values have single-element domains)
   - Track remaining legal values for unassigned variables

2. **Constraint Checking**
   - Implement a function to check if assigning a value violates Sudoku constraints
   - A cell's peers are all cells in the same row, column, or 3x3 box (excluding itself)

3. **Backtracking Search**
   - Select an unassigned variable
   - Try values from its domain
   - Recursively solve with the assignment
   - Backtrack if no solution found

4. **Variable Selection (if `use_mrv=True`)**
   - **Minimum Remaining Values (MRV)**: Choose the variable with the fewest legal values remaining
   - This reduces the branching factor by failing faster

5. **Value Ordering (if `use_lcv=True`)**
   - **Least Constraining Value (LCV)**: Order values by how many choices they eliminate for neighboring variables
   - Prefer values that leave the most flexibility for other variables

6. **Forward Checking (if `use_fc=True`)**
   - When assigning a value, remove it from the domains of all peer variables
   - Detect immediate failures when any domain becomes empty
   - Restore domains when backtracking

7. **Arc Consistency (if `use_ac3=True`)**
   - Run AC-3 as preprocessing before search
   - Optionally maintain arc consistency during search
   - An arc (Xi, Xj) is consistent if for every value in Xi's domain, there exists a compatible value in Xj's domain

### Implementation Tips

- **Do not mutate the input grid**. Work with your own domain representation.
- **Test incrementally**: Start with basic backtracking, then add one optimization at a time.
- **Handle edge cases**: Empty domains mean no solution exists at that branch.
- **Domain restoration**: When backtracking, carefully restore domains to their previous state.
- **MRV tie-breaking**: If multiple variables have the same domain size, any consistent choice is acceptable.
- **AC-3 algorithm**: Use a queue of arcs; when a domain changes, re-add arcs pointing to neighbors.

### Testing Strategy

1. **Start simple**: Implement basic backtracking without any optimizations
2. **Test with easy puzzles**: Use the GUI to load and solve simpler puzzles
3. **Add MRV**: Should reduce search time significantly
4. **Add Forward Checking**: Should further improve performance
5. **Add LCV and AC-3**: Fine-tune for maximum efficiency

The GUI displays solving time in milliseconds. Use this to compare optimization effectiveness.

### Expected Behavior

- **Without optimizations**: Basic backtracking should solve easy-to-medium puzzles in a few seconds
- **With MRV**: Should solve most puzzles in under a second
- **With MRV + FC**: Should solve hard puzzles efficiently
- **With all optimizations**: Near-instant solutions for most puzzles

### Example Usage

```python
from sudoku.csp import solve

# Empty cells are '0', given cells are '1'-'9'
grid = [
    ['5','3','0','0','7','0','0','0','0'],
    ['6','0','0','1','9','5','0','0','0'],
    # ... 7 more rows
]

# Solve with all optimizations
solution = solve(grid, use_mrv=True, use_lcv=True, use_fc=True, use_ac3=True)

if solution:
    print("Solved!")
    for row in solution:
        print(' '.join(row))
else:
    print("No solution exists")
```

## Common Pitfalls

1. **Modifying domains incorrectly**: Always restore domains when backtracking
2. **Inconsistent constraint checking**: Make sure peers() includes all cells that share a row, column, or box
3. **AC-3 infinite loops**: Ensure you don't re-add the same arc unless a domain actually changed
4. **Forgetting edge cases**: Handle single-cell domains, empty domains, and already-solved puzzles
5. **Type mismatches**: Input and output use strings ('0'-'9'), not integers

## Debugging Tips

- Use the GUI's "Auto Notes" feature to visualize possible values
- Print domain sizes at each recursive call to track MRV decisions
- Validate your constraint checking with the "Validate" button
- Test with easier puzzles first (earlier puzzles in the list tend to be easier)
- Add assertions to check domain consistency

## Assignment Requirements

Your `solve` function must:
- Correctly solve valid Sudoku puzzles
- Return `None` for unsolvable puzzles
- Respect all four optimization flags independently
- Complete in reasonable time (under 10 seconds for hard puzzles with optimizations)
- Pass all provided test cases

## Resources

- **CSP Chapter**: Review your textbook's chapter on constraint satisfaction
- **Sudoku Rules**: Each row, column, and 3x3 box must contain digits 1-9 exactly once
- **AC-3 Algorithm**: Maintain arc consistency by propagating constraints through a queue

## Getting Help

If you encounter issues:
1. Test your constraint checking function independently
2. Verify domain initialization with simple test cases
3. Add print statements to trace backtracking decisions
4. Start with all flags set to `False` and add optimizations incrementally
5. Use the GUI to visually debug your solver's behavior

Good luck, and happy coding!
