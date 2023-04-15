from ortools.linear_solver import pywraplp

from helpers.mytime import time_ms

from .mcsp import MCSP


class CommonSubstring(MCSP):
    def __init__(self, S1: str, S2: str) -> None:
        super().__init__(S1, S2)
        self.Q = [self.gen_substring_pos(self.S1, self.T), self.gen_substring_pos(self.S2, self.T)]
    
    def gen_substring_pos(self, s: str, T: set[str]) -> dict[str, list[tuple[int,int]]]:
        res: dict[str, list[tuple[int,int]]] = {}

        for i in range(len(s)):
            for j in range(i+1,len(s)+1):
                if s[i:j] in T:
                    if s[i:j] in res:
                        res[s[i:j]].append((i,j))
                    else:
                        res[s[i:j]] = [(i,j)]
        return res
    
    def solve(self, solverName: str, limit: int, heuristic: callable = None) -> tuple[float, int, int]:
        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(solverName)
        
        if limit is not None:
            print(f'Set limit to {limit}')
            solver.set_time_limit(limit)
          
        print("initializing the variables")
        y = {}
        for t_idx, t in enumerate(self.T):
            for q_idx,q in enumerate(self.Q):
                for k in q[t]:
                    y[t_idx,q_idx,k[0],k[1]] = solver.BoolVar(f'y[{q_idx},{t_idx},{k[0]},{k[1]}]')
        
            
        print("First constraint")
        for t_idx, t in enumerate(self.T):
            partitions_of_S1 = [ y[t_idx, 0, k[0], k[1]] for k in self.Q[0][t] ]
            partitions_of_S2 = [ y[t_idx, 1, k[0], k[1]] for k in self.Q[1][t] ]

            solver.Add(solver.Sum(partitions_of_S1) == solver.Sum(partitions_of_S2))
            
        print("Second contraint")
        for j in range(self.N):
            substrings_at_pos_j_of_S1 = []
            for t_idx, t in enumerate(self.T):
                for k in self.Q[0][t]: 
                    if k[0] <= j < k[1]: # k[1] == k[0] + size(t)
                        substrings_at_pos_j_of_S1.append(y[t_idx,0,k[0],k[1]])
            solver.Add(solver.Sum(substrings_at_pos_j_of_S1) == 1)
            
        print("Third constraint")
        for j in range(self.N):
            substrings_at_pos_j_of_S2 = []
            for t_idx, t in enumerate(self.T):
                for k in self.Q[1][t]:
                    if k[0] <= j < k[1]: # k[1] == k[0] + size(t)
                        substrings_at_pos_j_of_S2.append(y[t_idx,1,k[0],k[1]])
            solver.Add(solver.Sum(substrings_at_pos_j_of_S2) == 1)
             
        print("Objective functions")
        objective_terms = []
        for t_idx, t in enumerate(self.T):
            for k in self.Q[0][t]:
                objective_terms.append(y[t_idx, 0, k[0], k[1]])

        solver.Minimize(solver.Sum(objective_terms))

        if heuristic is not None:
            print('Using heuristic')
            variables = []
            fsol = heuristic(self.S1, self.S2)
            for t_idx, t in enumerate(self.T):
                if t in fsol:
                    for b in fsol[t]:
                        for k in self.Q[0][t]:
                            if k[0] == b[0]:
                                variables.append(y[t_idx, 0, k[0], k[1]])
                        for k in self.Q[1][t]:
                            if k[0] == b[1]:
                                variables.append(y[t_idx, 1, k[0], k[1]])
            solver.SetHint(variables, [1]*len(variables))
        
        print("Start solving")
        st = time_ms()
        status = solver.Solve()
        et = time_ms() - st
        print('Finished Solving')

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            val = solver.Objective().Value()
            val_status = 0 if status == pywraplp.Solver.OPTIMAL else 1
        else:
            val = -1.0
            val_status = -1

        return round(val,2), int(et), val_status