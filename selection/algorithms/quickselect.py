import random  # randomised quickselect by dylan costa, expected o(n) worst o(n^2)


def select(a, k, rng=random):  # gives back the k-th smallest in a (counting from 0)
    if not 0 <= k < len(a):
        raise IndexError("k out of range")

    while True:
        if len(a) <= 5:
            return sorted(a)[k]  # small list so just sort it
        pivot = a[rng.randrange(len(a))]  # pick a random pivot
        lows = [x for x in a if x < pivot]  # everything smaller than pivot

        if k < len(lows):
            a = lows  # answer is in the smaller bit
            continue
        nEqual = len(a) - len(lows) - sum(1 for x in a if x > pivot)  # how many equal the pivot, stops it going slow with loads of duplicates

        if k < len(lows) + nEqual:
            return pivot  # answer is the pivot
        k -= len(lows) + nEqual  # move k along for the bigger bit
        a = [x for x in a if x > pivot]  # everything bigger than pivot