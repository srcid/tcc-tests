from time import time_ns
from typing import Dict, List, Set, Tuple

from ortools.linear_solver import pywraplp

from .mcsp import MCSP


class CommonSubstring(MCSP):
    def __init__(self, S1: str, S2: str) -> None:
        super().__init__(S1, S2)
        self.Q = [self.gen_substring_pos(self.S1, self.T), self.gen_substring_pos(self.S2, self.T)]
    
    def gen_substring_pos(self, s: str, T: Set[str]) -> Dict[str, List[Tuple[int,int]]]:
        res: Dict[str, List[Tuple[int,int]]] = {}

        for i in range(len(s)+1):
            for j in range(i+1,len(s)+1):
                if s[i:j] in T:
                    if s[i:j] in res:
                        res[s[i:j]].append((i,j))
                    else:
                        res[s[i:j]] = [(i,j)]
        return res
    
    def solve(self, solverName: str):
        solver = pywraplp.Solver.CreateSolver(solverName)
        if solver is None:
            return
          
        # initializing the variables
        y = {}
        for t_idx, t in enumerate(self.T):
            for q_idx,q in enumerate(self.Q):
                for k in q[t]:
                    y[t_idx,q_idx,k[0],k[1]] = solver.BoolVar(f'y[{q_idx},{t_idx},{k[0]},{k[1]}]')
        
            
        # first constraint
        for t_idx, t in enumerate(self.T):
            partitions_of_S1 = [ y[t_idx, 0, k[0], k[1]] for k in self.Q[0][t] ]
            partitions_of_S2 = [ y[t_idx, 1, k[0], k[1]] for k in self.Q[1][t] ]

            solver.Add(solver.Sum(partitions_of_S1) == solver.Sum(partitions_of_S2))
            
        # second contraint            
        for j in range(self.N):
            substrings_at_pos_j_of_S1 = []
            for t_idx, t in enumerate(self.T):
                for k in self.Q[0][t]: 
                    if k[0] <= j < k[1]: # k[1] == k[0] + size(t)
                        substrings_at_pos_j_of_S1.append(y[t_idx,0,k[0],k[1]])
            solver.Add(solver.Sum(substrings_at_pos_j_of_S1) == 1)
            
        # third constraint
        for j in range(self.N):
            substrings_at_pos_j_of_S2 = []
            for t_idx, t in enumerate(self.T):
                for k in self.Q[1][t]:
                    if k[0] <= j < k[1]: # k[1] == k[0] + size(t)
                        substrings_at_pos_j_of_S2.append(y[t_idx,1,k[0],k[1]])
            solver.Add(solver.Sum(substrings_at_pos_j_of_S2) == 1)
             
        # objective functions
        objective_terms = []
        for t_idx, t in enumerate(self.T):
            for k in self.Q[0][t]:
                objective_terms.append(y[t_idx, 0, k[0], k[1]])

        solver.Minimize(solver.Sum(objective_terms))
        
        st = time_ns() * 1e-6
        status = solver.Solve()
        et = time_ns() * 1e-6 - st

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            val = solver.Objective().Value()
        else:
            val = -1

        return round(val,1), round(et,4)