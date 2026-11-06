# Selection: quickselect vs median of medians

programming assignment 2, theme 2 (deterministic vs randomised). solo project by Dylan Costa.

finds the k-th smallest number in a unsorted list two ways:
- `algorithms/quickselect.py` - random pivot, O(n) on average
- `algorithms/median_of_medians.py` - median of medians pivot, O(n) always

`sorted(a)[k]` is there as well to compare against.

## how to run it
needs python 3.10+ and matplotlib (`pip install matplotlib`).
```
python test_correctness.py     # checks both are right
python benchmark.py            # runs everything (about 3 mins), saves to results/
python benchmark.py --quick    # quicker smaller version
```