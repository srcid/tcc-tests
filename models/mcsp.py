from typing import Set


class MCSP:
    def __init__(self, S1:str, S2:str) -> None:
        if len(S1) != len(S2):
            raise 'Invalid input strings: S1 and S2 must have the same size'
        
        SUBS_OF_S1 = self.gen_substring_set(S1)
        SUBS_OF_S2 = self.gen_substring_set(S2)
        
        self.S1 = S1
        self.S2 = S2
        self.N = len(S1)
        self.T = set.intersection(SUBS_OF_S1, SUBS_OF_S2)

    def gen_substring_set(self, s: str) -> Set[str]:
        res: Set[str] = set()

        for i in range(len(s)):
            for j in range(i+1,len(s)+1):
                res.add(s[i:j])

        return res