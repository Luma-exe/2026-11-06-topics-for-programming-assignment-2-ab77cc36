# Randomised vs deterministic selection: quickselect and median of medians

**Author:** Dylan Costa 

## 1. The problem and the algorithms

you get a list of n numbers and a rank k and you have to find the k-th smallest one (k = n/2 is the median). sorting does it in O(n log n) but both of these do it in O(n).

both pick a pivot, split the list into smaller, equal and bigger, then only carry on in the side the answer is in. the only difference is how they pick the pivot.

- **quickselect** picks a random pivot. on average the list shrinks to 3/4 or less each round so its O(n) expected. the worst case is O(n^2) but the chance of that is tiny and no input can force it.
- **median of medians** splits the list into groups of 5, takes the median of each group, then finds the median of them. this pivot always has about 3n/10 elements on each side so T(n) <= T(n/5) + T(7n/10) + O(n), which is O(n) even in the worst case.

both use the same partition code, and the equal bucket stops lists with loads of duplicates going slow.

## 2. Predictions (before running anything)

1. quickselect will be about 2-5x faster than median of medians, cos median of medians does way more work to pick its pivot.
2. time per element will be flat for both as n gets bigger.
3. `sorted()` is written in C so it will win when n is small, but both will beat it from around n = 10^3-10^4.
4. input order wont matter to either one, and duplicates will make them faster.
5. quickselect will sometimes be 2-3x slower than normal but never close to O(n^2).
6. quickselect will be faster when k is near the start or end, median of medians wont care.

## 3. How i tested it

i5-13600KF, 32 GB RAM, windows 11, python 3.13. each time is the median of 21 runs (7 for big n) using `time.perf_counter()`, with a fresh copy of the list each run that isnt timed. all inputs come from the fixed seed 12345.

inputs: random, sorted, reversed, organ pipe (up then down), 10 distinct values, all equal.

experiments:
1. scaling: n from 10^3 to 10^6
2. input types at n = 200,000
3. 2000 runs on the same input to see the spread
4. different values of k at n = 100,000

## 4. Results

### 4.1 Scaling

| n | quickselect | median of medians | sorted()[k] |
|---|---|---|---|
| 10^3 | 0.13 ms | 0.26 ms | 0.05 ms |
| 10^4 | 0.96 ms | 2.67 ms | 0.74 ms |
| 10^5 | 12.8 ms | 28.2 ms | 10.3 ms |
| 3*10^5 | 26.0 ms | 86.2 ms | 35.0 ms |
| 10^6 | 112 ms | 302 ms | 142 ms |

both are linear. median of medians is 2.2-3.3x slower cos it does all the same work plus sorting groups of 5 and an extra recursive call. `sorted()` beats both up to about 10^5, and median of medians never beats it at all.

### 4.2 Input types (n = 200,000)

| input | quickselect | median of medians | sorted()[k] |
|---|---|---|---|
| random | 24.1 ms | 57.2 ms | 21.8 ms |
| sorted | 16.7 ms | 43.9 ms | 0.69 ms |
| reversed | 17.8 ms | 45.4 ms | 0.84 ms |
| organ pipe | 18.0 ms | 44.2 ms | 1.03 ms |
| 10 distinct values | 15.6 ms | 34.7 ms | 9.1 ms |
| all equal | 4.0 ms | 13.9 ms | 0.52 ms |

order didnt hurt either of them, they were actually about 25% faster on ordered input. duplicates made both faster like i thought. `sorted()` is way faster on ordered input cos timsort spots runs that are already sorted.

### 4.3 Spread over 2000 runs (n = 100,000)

| | median | 99th percentile | max |
|---|---|---|---|
| quickselect | 11.5 ms | 23.4 ms | 29.6 ms |
| median of medians | 51.3 ms | 102 ms | 267 ms |

quickselects slowest run was only 2.6x its median, nowhere near O(n^2).

### 4.4 Rank

quickselect was about 4x faster at k = 0 (5.5 ms) than at k = n/2 (about 20 ms). median of medians stayed roughly the same (37-63 ms). the times are a bit higher than the scaling test, i think thats just the computer being noisy.

## 5. What surprised me

1. **sorting beat both O(n) algorithms for most sizes.** its because `sorted()` runs in C and mine run in python, so each step costs way more. big O only really compares things written the same way.
2. **sorting was about 25x faster on ordered input**, cos timsort uses the order thats already there and my algorithms dont.
3. **the deterministic one had the worse spread** (5.2x vs 2.6x). it does the same steps every time but the computer doesnt, and longer runs get hit by more stuff like the garbage collector.

## 6. What i would do next

- count comparisons as well as time
- try introselect (quickselect that switches to median of medians if it goes too deep)
- try writing it in C to get rid of the python overhead

## 7. Individual contributions

solo project. I Dylan Costa did the code, tests, experiments, report and video.

## 8. AI use

AI was utilised to assit with planning of the code base and writing the code it was also used to check over both markdown files to correct formatting and ensure the assessment was completed.