from .overlaps import overlaps


def longest_common_substring_without_overlapping(S1: str, S2: str, blocks: dict[str, list[tuple[int, int]]]) -> tuple[str, int, int]:
    """
    Return the longest common substring of two strings without overlaping
    substrings in blocks and its start index at S1 and S2
    """
    m, n = len(S1), len(S2)
    # Initialize a matrix with 0s
    lcs_matrix = [[0]*(n+1) for i in range(m+1)]
    # Keep track of the length and position of longest substring found
    max_len = 0
    end_pos_S1 = 0
    end_pos_S2 = 0
    # Fill in the matrix
    for i in range(1, m+1):
        for j in range(1, n+1):
            if S1[i-1] == S2[j-1] and not overlaps(i-1, j-1, blocks):
                lcs_matrix[i][j] = lcs_matrix[i-1][j-1] + 1
                if lcs_matrix[i][j] > max_len:
                    max_len = lcs_matrix[i][j]
                    end_pos_S1 = i
                    end_pos_S2 = j
            else:
                lcs_matrix[i][j] = 0
    
    # Retrieve the longest common substring
    start_pos_S1 = end_pos_S1 - max_len
    start_pos_S2 = end_pos_S2 - max_len
    
    return S1[start_pos_S1:end_pos_S1], start_pos_S1, start_pos_S2
    