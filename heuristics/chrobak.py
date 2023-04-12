from helpers.longest_common_substring_without_overlapping import (
    longest_common_substring_without_overlapping,
)


def chrobak(S1: str, S2: str):
    """
    Returns a feasible solution for MSCP problem instance
    """
    blocks: dict[str, list[tuple[int, int]]] = {}
    acc = 0
    while acc < len(S1):
        s, pos_in_S1, pos_in_S2 = longest_common_substring_without_overlapping(S1, S2, blocks)
        if s not in blocks.keys():
            blocks[s] = []
        blocks[s].append((pos_in_S1, pos_in_S2))
        acc += len(s)

    return blocks
