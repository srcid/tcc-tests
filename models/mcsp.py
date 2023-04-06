class MCSP:
    def __init__(self, S1:str, S2:str) -> None:
        if len(S1) != len(S2):
            raise 'Invalid input strings: S1 and S2 must have the same size'
        
        self.S1: str = S1
        self.S2: str = S2
        self.N: int = len(S1)
        self.T: set[str] = self.gen_common_substring_set(S1, S2)

    def gen_substring_set(self, s: str) -> set[str]:
        """
        Generate a set of all substrings of s
        """
        res: set[str] = set()

        for i in range(len(s)):
            for j in range(i+1,len(s)+1):
                res.add(s[i:j])

        return res
    
    def gen_common_substring_set(self, S1: str, S2: str) -> set[str]:
        """
        Generate a set of all (unique) strings that appear as substrings at 
        least once in both S1 and S2
        """
        SUBS_OF_S1: set[str] = self.gen_substring_set(S1)
        SUBS_OF_S2: set[str] = self.gen_substring_set(S2)

        return set.intersection(SUBS_OF_S1, SUBS_OF_S2)