from .overlaps import overlaps


def longest_common_substring_without_overlaping(S1: str, S2: str, blocks: dict[str, list[tuple[int, int]]]) -> tuple[str, int, int]:
    """
    Return the longest common substring without overlaping substrings in blocks
    and its start index at S1 and S2
    """
    pos_in_S1 = -1
    pos_in_S2 = -1
    longest = ''

    for i in range(len(S1)):
        for j in range(len(S2)):
            if S1[i] == S2[j] and not overlaps(i, j, blocks):
                length = 1
                while (i + length) < len(S1) and (j + length) < len(S2) and S1[i + length] == S2[j + length] and not overlaps(i + length, j + length, blocks):
                    length = length + 1
                if length > len(longest):
                    longest = S1[i: i + length]
                    pos_in_S1 = i
                    pos_in_S2 = j
    
    return longest, pos_in_S1, pos_in_S2
