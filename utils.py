from typing import List


def diff(list1, list2):
    """Computes the (set) difference between two lists."""
    return list(set(list1) - set(list2))


def chunk(l: List, n: int) -> List[List]:
    """Returns list of n-sized lists from l or one list of size
    len(l) if list length is smaller than n."""
    if len(l) < n:
        return [l]

    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]
