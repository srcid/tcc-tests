from pytest import mark

from helpers.overlaps import overlaps


@mark.parametrize(
    'pos_in_S1,pos_in_S2,blocks,expected_res', [
        # string "abc" at (2,5) in S1 and (0,3) in S2
        *[(2+i, 0+i, {'abcdabc': [(2, 4)],'c': [(0, 2)]}, True) for i in range(3)],
        # string "cdab" at (0,4) in S1 and (6,10) in S2
        *[(0+i, 6+i, {'abcdabc': [(2, 4)],'c': [(0, 2)]}, True) for i in range(4)],
        # string "ab" at (10,12) in S1 and (0,2) in S2
        *[(10+i, 0+i, {'abcdabc': [(2, 4)],'c': [(0, 2)]}, False) for i in range(2)],
        # string "cea" at (8,11)  in S1 and (2,5) in S2
        (8, 2, {'abcdabc': [(2, 4)],'c': [(0, 2)]}, True),
        (9, 3, {'abcdabc': [(2, 4)],'c': [(0, 2)]}, False),
        (10, 4, {'abcdabc': [(2, 4)],'c': [(0, 2)]}, True)
    ]
)
def test_overlaps(pos_in_S1, pos_in_S2, blocks, expected_res):
    res = overlaps(pos_in_S1, pos_in_S2, blocks)
    
    assert res == expected_res


