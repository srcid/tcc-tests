from helpers.longest_common_substring_without_overlaping import (
    longest_common_substring_without_overlaping,
)


def test_strings_cdabcdabceab_abceabcdabcd_case_blocks_is_empty():
    S1, S2 = "cdabcdabceab", "abceabcdabcd"
    blocks: dict[str, list[tuple[int,int]]] = {}

    expected_res = ('abcdabc', 2, 4)
    res = longest_common_substring_without_overlaping(S1, S2, blocks)

    assert(res == expected_res)

def test_strings_cdabcdabceab_abceabcdabcd_case_blocks_has_abcdabc_2_4():
    S1, S2 = "cdabcdabceab", "abceabcdabcd"
    blocks: dict[str, list[tuple[int,int]]] = {
        'abcdabc': [(2, 4)]
    }

    expected_res = ('ab', 10, 0)
    res = longest_common_substring_without_overlaping(S1, S2, blocks)

    assert(res == expected_res)

def test_strings_cdabcdabceab_abceabcdabcd_case_blocks_has_abcdabc_2_4_ab_10_0():
    S1, S2 = "cdabcdabceab", "abceabcdabcd"
    blocks: dict[str, list[tuple[int,int]]] = {
        'abcdabc': [(2, 4)],
        'ab': [(10, 0)]
    }

    expected_res = ('c', 0, 2)
    res = longest_common_substring_without_overlaping(S1, S2, blocks)

    assert(res == expected_res)
