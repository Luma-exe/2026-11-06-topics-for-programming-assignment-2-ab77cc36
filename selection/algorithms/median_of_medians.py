def select(a, k):  # median of medians by dylan costa, worst case o(n) every time
    if not 0 <= k < len(a):
        raise IndexError("k out of range")

    while True:
        if len(a) <= 5:
            return sorted(a)[k]  # small list so just sort it
        pivot = medianOfMedians(a)  # pivot always has about 3n/10 on each side
        lows = [x for x in a if x < pivot]  # everything smaller than pivot

        if k < len(lows):
            a = lows  # answer is in the smaller bit
            continue
        nEqual = len(a) - len(lows) - sum(1 for x in a if x > pivot)  # how many equal the pivot

        if k < len(lows) + nEqual:
            return pivot  # answer is the pivot
        k -= len(lows) + nEqual  # move k along for the bigger bit
        a = [x for x in a if x > pivot]  # everything bigger than pivot, at most about 7n/10 left


def medianOfMedians(a):
    medians = [sorted(a[i:i + 5])[(len(a[i:i + 5]) - 1) // 2]  # median of each group of 5
               for i in range(0, len(a), 5)]
    return select(medians, (len(medians) - 1) // 2)  # median of them medians, t(n) <= t(n/5) + t(7n/10) + o(n) so its o(n)