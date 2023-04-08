from heuristics.chrobak import chrobak


def test_chrobak_cdabcdabceab_abceabcdabcd():
    expected_res = {'abcdabc': [(2, 4)], 
                    'ab': [(10, 0)], 
                    'c': [(0, 2)], 
                    'd': [(1, 11)], 
                    'e': [(9, 3)]}
    res = chrobak("cdabcdabceab", "abceabcdabcd")
    
    assert res == expected_res