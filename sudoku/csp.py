from typing import List, Set, Dict, Tuple, Optional
import copy


def solve(grid: List[List[str]], *, use_mrv: bool = False, use_lcv: bool = False, 
            use_fc: bool = False, use_ac3: bool = False) -> Optional[List[List[str]]]:
    """
    Solve a Sudoku puzzle using CSP backtracking with optional optimizations.
    
    Args:
        grid: 9x9 grid where each cell is a string '0'-'9' ('0' means empty)
        use_mrv: If True, use Minimum Remaining Values heuristic for variable selection
        use_lcv: If True, use Least Constraining Value heuristic for value ordering
        use_fc: If True, use Forward Checking during search
        use_ac3: If True, use AC-3 algorithm for initial constraint propagation
    
    Returns:
        Solved 9x9 grid as list of lists of strings, or None if no solution exists
    
    Example:
        >>> grid = [['5','3','0', ...], ...]  # 0 represents empty cells
        >>> solution = solve(grid, use_mrv=True, use_fc=True)
    """
    # Initialize the CSP
    csp = SudokuCSP(grid)
    
    # Apply AC-3 if requested for initial constraint propagation
    if use_ac3:
        if not csp.ac3():
            return None  # No solution exists
        
    # Solve using backtracking with specified heuristics
    if csp.backtrack(use_mrv=use_mrv, use_lcv=use_lcv, use_fc=use_fc):
        return csp.get_solution()
    return None  # No solution found


class SudokuCSP:
    """
    Represents a Sudoku puzzle as a Constraint Satisfaction Problem.
    
    Variables: Each empty cell (r, c) in the 9x9 grid
    Domain: Numbers 1-9 for each variable
    Constraints: Sudoku rules (row, column, and 3x3 box uniqueness)
    """
    
    def __init__(self, grid: List[List[str]]):
        """
        Initialize the CSP from a Sudoku grid.
        
        Args:
            grid: 9x9 grid where '0' represents an empty cell
        """
        self.size = 9
        self.grid = [row[:] for row in grid]  # Deep copy
        
        # Initialize domains for each cell
        # domains[r][c] is a set of possible values for cell (r, c)
        self.domains: List[List[Set[int]]] = [[set() for _ in range(9)] for _ in range(9)]
        
        for r in range(9):
            for c in range(9):
                if grid[r][c] == '0':
                    # Empty cell: calculate possible values
                    self.domains[r][c] = self._get_legal_values(r, c)
                else:
                    # Given cell: domain is the single given value
                    self.domains[r][c] = {int(grid[r][c])}
                    
    def _get_legal_values(self, row: int, col: int) -> Set[int]:
        """
        Get all legal values for a cell based on current assignments.
        
        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            
        Returns:
            Set of integers 1-9 that don't violate Sudoku constraints
        """
        # TODO
        raise NotImplementedError()
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get all cells that are constrained with the given cell.
        
        Neighbors are cells in the same row, column, or 3x3 box.
        
        Args:
            row: Row index (0-8)
            col: Column index (0-8)
            
        Returns:
            List of (row, col) tuples representing neighbor cells
        """
        # TODO
        raise NotImplementedError()
    
    def select_unassigned_variable(self, use_mrv: bool) -> Optional[Tuple[int, int]]:
        """
        Select the next variable (empty cell) to assign.
        
        Args:
            use_mrv: If True, use Minimum Remaining Values heuristic
                    (select variable with fewest legal values)
                    If False, select first unassigned variable
        
        Returns:
            (row, col) tuple of selected cell, or None if all assigned
        """
        # TODO
        raise NotImplementedError()
    
    def order_domain_values(self, row: int, col: int, use_lcv: bool) -> List[int]:
        """
        Order the values in the domain of a variable.
        
        Args:
            row: Row index of the variable
            col: Column index of the variable
            use_lcv: If True, use Least Constraining Value heuristic
                    (order values by how much they constrain neighbors)
                    If False, use arbitrary ordering
        
        Returns:
            List of values from the domain, ordered appropriately
        """
        # TODO
        raise NotImplementedError()
    
    def is_consistent(self, row: int, col: int, value: int) -> bool:
        """
        Check if assigning a value to a cell is consistent with constraints.
        
        Args:
            row: Row index
            col: Column index
            value: Value to assign (1-9)
        
        Returns:
            True if assignment doesn't violate any constraints
        """
        # TODO
        raise NotImplementedError()
    
    def forward_check(self, row: int, col: int, value: int) -> Optional[Dict]:
        """
        Perform forward checking after assigning a value to a cell.
        
        Forward checking removes the assigned value from domains of all neighbors.
        If any neighbor's domain becomes empty, the assignment is invalid.
        
        Args:
            row: Row index of assigned variable
            col: Column index of assigned variable
            value: Assigned value
        
        Returns:
            Dictionary mapping (r,c) -> removed_values for rollback,
            or None if forward checking detects inconsistency
        """
        # TODO
        raise NotImplementedError()
    
    def restore_domains(self, removed: Dict[Tuple[int, int], Set[int]]):
        """
        Restore domains after backtracking (undo forward checking).
        
        Args:
            removed: Dictionary from forward_check() mapping cells to removed values
        """
        # TODO
        raise NotImplementedError()
    
    def ac3(self) -> bool:
        """
        Apply AC-3 (Arc Consistency 3) algorithm for constraint propagation.
        
        AC-3 enforces arc consistency by iteratively removing values from domains
        that cannot be part of any solution. This is more powerful than forward
        checking as it propagates constraints through the entire network.
        
        Returns:
            True if the CSP is arc-consistent (may have solution),
            False if inconsistency detected (no solution possible)
        """
        # TODO
        raise NotImplementedError()
    
    def _revise(self, xi: Tuple[int, int], xj: Tuple[int, int]) -> bool:
        """
        Revise the domain of Xi to make it consistent with Xj.
        
        Remove values from Xi's domain that have no consistent value in Xj's domain.
        
        Args:
            xi: (row, col) of first variable
            xj: (row, col) of second variable
        
        Returns:
            True if Xi's domain was revised (values removed), False otherwise
        """
        # TODO
        raise NotImplementedError()
    
    def backtrack(self, use_mrv: bool = False, use_lcv: bool = False, 
                    use_fc: bool = False) -> bool:
        """
        Recursive backtracking search to solve the CSP.
        
        Args:
            use_mrv: Use Minimum Remaining Values heuristic for variable selection
            use_lcv: Use Least Constraining Value heuristic for value ordering
            use_fc: Use Forward Checking for constraint propagation
        
        Returns:
            True if solution found, False otherwise
        """
        # TODO
        raise NotImplementedError()
    
    def get_solution(self) -> List[List[str]]:
        """
        Get the current grid as the solution.
        
        Returns:
            9x9 grid as list of lists of strings
        """
        return [row[:] for row in self.grid]