from ortools.linear_solver import pywraplp

from helpers.mytime import time_ms

from .mcsp import MCSP


class CommonBlocks(MCSP):
    def __init__(self, S1: str, S2: str) -> None:
        super().__init__(S1, S2)
        self.B = self.gen_common_blocks(self.S1, self.S2, self.T)

    def get_ocurrence_indices(self, S: str, pattern: str) -> list[int]:
        res = []
        for i in range(len(S)):
            if S[i:i+len(pattern)] == pattern:
                res.append(i)
        return res

    def gen_common_blocks(self, S1: str, S2: str, T: set[str]) -> dict[str, list[tuple[int,int]]]:
        blocks: dict[str, list[tuple[int,int]]] = {}
        
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
    
    def solve(self, solverName: str, limit: int, heuristic: callable = None) -> tuple[float, int, int]:
        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver(solverName)
        
        if limit is not None:
            print(f'Set time limit to {limit}')
            solver.set_time_limit(limit)
        
        print('Initializing the variables')
        x = {}
        for t_idx, t in enumerate(self.T):
            for b in self.B[t]:
                x[t_idx,b[0],b[1]] = solver.BoolVar(f'x[{t_idx},{b[0]},{b[1]}]')
        
        print('First constraint')
        for j in range(self.N):
            blocks_at_pos_j = []
            for t_idx, t in enumerate(self.T):
                for b in self.B[t]:
                    if b[0] <= j < (b[0] + len(t)):
                        blocks_at_pos_j.append(x[t_idx, b[0], b[1]])
            solver.Add(solver.Sum(blocks_at_pos_j) == 1)
        
        print('Second contraint')
        for j in range(self.N):
            blocks_at_pos_j = []
            for t_idx, t in enumerate(self.T):
                for b in self.B[t]:
                    if b[1] <= j < (b[1] + len(t)):
                        blocks_at_pos_j.append(x[t_idx, b[0], b[1]])
            solver.Add(solver.Sum(blocks_at_pos_j) == 1)
            
        print('Objective functions')
        objetive_terms = []
        for t_idx, t in enumerate(self.T):
            for b in self.B[t]:
                objetive_terms.append(x[t_idx,b[0],b[1]])
        solver.Minimize(solver.Sum(objetive_terms))

        if heuristic is not None:
            print('Using heuristic')
            fsol = heuristic(self.S1, self.S2)
            variables = []
            for t_idx, t in enumerate(self.T):
                if t in fsol:
                    for b in fsol[t]:
                        variables.append(x[t_idx, b[0], b[1]])
            solver.SetHint(variables, [1]*len(variables))

        print('Starting Solving')
        st = time_ms()
        status = solver.Solve()
        et = time_ms() - st
        print('Finished solving')

        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            val = solver.Objective().Value()
            val_status = 0 if status == pywraplp.Solver.OPTIMAL else 1
        else:
            val = -1.0
            val_status = -1

        return round(val,2), int(et), val_status
