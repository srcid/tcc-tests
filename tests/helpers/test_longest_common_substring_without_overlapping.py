from pytest import mark

from helpers.longest_common_substring_without_overlapping import (
    longest_common_substring_without_overlapping,
)


@mark.parametrize(
      'S1,S2,blocks,expected_res', [
        ("ABCDGH","ACDGHR", {}, ('CDGH', 2, 1)),
        ("cdabcdabceab", "abceabcdabcd", {}, ('abcdabc', 2, 4)),
        ("cdabcdabceab", "abceabcdabcd", {'abcdabc': [(2, 4)]}, ('ab', 10, 0)),
        ("cdabcdabceab", "abceabcdabcd", {'abcdabc': [(2, 4)],
                                          'ab': [(10, 0)]}, ('c', 0, 2)), 
        ("cdabcdabceab", "abceabcdabcd", {'abcdabc': [(2, 4)],
                                          'ab': [(10, 0)],
                                          'c': [(0,2)],
                                          'd': [(1,11)]}, ('e', 9, 3)),
        ("cdabcdabceab", "abceabcdabcd", {'abcdabc': [(2, 4)],
                                          'ab': [(10, 0)],
                                          'c': [(0,2)],
                                          'd': [(1,11)],
                                          'e': [(9,3)],}, ('',0,0))
      ]
)
def test_longest_common_substring_without_overlapping(S1, S2, blocks, expected_res):
    res = longest_common_substring_without_overlapping(S1, S2, blocks)
    assert res == expected_res
