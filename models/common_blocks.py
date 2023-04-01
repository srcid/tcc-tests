from time import time_ns
from typing import Dict, List, Set, Tuple

from ortools.linear_solver import pywraplp

from .mcsp import MCSP


class CommonBlocks(MCSP):
    def __init__(self, S1: str, S2: str) -> None:
        super().__init__(S1, S2)
        self.B = self.gen_common_blocks(self.S1, self.S2, self.T)

    def get_ocurrence_indices(self, S: str, pattern: str):
        res = []
        for i in range(len(S)):
            if S[i:i+len(pattern)] == pattern:
                res.append(i)
        return res

    def gen_common_blocks(self, S1: str, S2: str, T: Set[str]) -> Dict[str, List[Tuple[int,int]]]:
        blocks: Dict[str, List[Tuple[int,int]]] = {}
        
        for t in T:
            pos_of_t_in_S1 = self.get_ocurrence_indices(S1, t)
            pos_of_t_in_S2 = self.get_ocurrence_indices(S2, t)
        
            for i in pos_of_t_in_S1:
                for j in pos_of_t_in_S2:
                    if t in blocks:
                        blocks[t].append((i,j))
                    else:
                        blocks[t] = [(i,j)]
                
        return blocks
    
    def solve(self, solverName: str):
        solver = pywraplp.Solver.CreateSolver(solverName)
        if solver is None:
            return
        
        # initializing the variables
        x = {}
        for t_idx, t in enumerate(self.T):
            for b in self.B[t]:
                x[t_idx,b[0],b[1]] = solver.BoolVar(f'x[{t_idx},{b[0]},{b[1]}]')
        
        # first constraint
        for j in range(self.N):
            blocks_at_pos_j = []
            for t_idx, t in enumerate(self.T):
                for b in self.B[t]:
                    if b[0] <= j < (b[0] + len(t)):
                        blocks_at_pos_j.append(x[t_idx, b[0], b[1]])
            solver.Add(solver.Sum(blocks_at_pos_j) == 1)
        
        # second contraint
        for j in range(self.N):
            blocks_at_pos_j = []
            for t_idx, t in enumerate(self.T):
                for b in self.B[t]:
                    if b[1] <= j < (b[1] + len(t)):
                        blocks_at_pos_j.append(x[t_idx, b[0], b[1]])
            solver.Add(solver.Sum(blocks_at_pos_j) == 1)
            
        # objective functions
        objetive_terms = []
        for t_idx, t in enumerate(self.T):
            for b in self.B[t]:
                objetive_terms.append(x[t_idx,b[0],b[1]])
        solver.Minimize(solver.Sum(objetive_terms))

        st = time_ns() * 1e-6
        status = solver.Solve()
        et = time_ns() * 1e-6 - st

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            val = solver.Objective().Value()
        else:
            val = -1

        return round(val,1), round(et,4)
