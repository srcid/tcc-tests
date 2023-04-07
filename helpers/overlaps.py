def overlaps(pos_in_S1: int, pos_in_S2: int, blocks: dict[str, list[tuple[int, int]]]) -> bool:
    """
    Return True if the char in pos_in_S1 at S1 string and pos_in_S2 at S2 string
    overlap any block in blocks
    """
    for s in blocks:
        for i, j in blocks[s]:
            if (i <= pos_in_S1 < (i + len(s)) or j <= pos_in_S2 < (j + len(s))):
                return True
    return False
