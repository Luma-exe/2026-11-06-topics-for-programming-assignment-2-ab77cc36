import random
from algorithms import quickselect, median_of_medians

def main():  # checks both against sorted() on loads of inputs
    rng = random.Random(0)
    cases = [[1], [2, 1], [5] * 50, list(range(100)), list(range(100, 0, -1))]  # edge cases

    for _ in range(500):
        n = rng.randint(1, 300)
        cases.append([rng.randint(0, rng.choice([3, 50, 10**9])) for _ in range(n)])  # random lists, some with lots of duplicates

    for a in cases:
        s = sorted(a)

        for k in {0, len(a) // 2, len(a) - 1, rng.randrange(len(a))}:  # min, middle, max and a random one
            assert quickselect.select(list(a), k) == s[k]
            assert median_of_medians.select(list(a), k) == s[k]
    print(f"OK: {len(cases)} inputs passed for both algorithms")

if __name__ == "__main__":
    main()