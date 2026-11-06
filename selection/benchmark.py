import csv, random, statistics, sys, time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from algorithms import quickselect, median_of_medians

QUICK = "--quick" in sys.argv  # use --quick for a smaller faster run
SEED = 12345  # fixed seed so the inputs are the same every time
ALGOS = {
    "quickselect (randomized)": quickselect.select,
    "median-of-medians (deterministic)": median_of_medians.select,
    "sorted()[k] baseline": lambda a, k: sorted(a)[k],  # just sorting it, to compare against
}

def timeit(fn, a, k, reps):  # median time of reps runs
    fn(list(a), k)  # warm up run, not timed
    ts = []

    for _ in range(reps):
        b = list(a)  # fresh copy each time, copying isnt timed
        t0 = time.perf_counter()
        fn(b, k)
        ts.append(time.perf_counter() - t0)
    return statistics.median(ts)

def families(n, rng):  # all the input types we test
    half = list(range(n // 2))
    return {
        "random": [rng.randint(0, 10**9) for _ in range(n)],
        "sorted": list(range(n)),
        "reversed": list(range(n, 0, -1)),
        "10 distinct values": [rng.randint(0, 9) for _ in range(n)],
        "all equal": [7] * n,
        "organ pipe": half + half[::-1],
    }

def writeCsv(name, header, rows):
    with open(f"results/{name}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

def expScaling(rng):  # time per element as n gets bigger
    sizes = [10**3, 3*10**3, 10**4, 3*10**4, 10**5, 3*10**5, 10**6]
    if QUICK: sizes = sizes[:4]
    rows = []

    for n in sizes:
        a = [rng.randint(0, 10**9) for _ in range(n)]
        reps = 21 if n <= 10**5 else 7

        for name, fn in ALGOS.items():
            t = timeit(fn, a, n // 2, reps)
            rows.append((name, n, t)); print(f"scaling n={n:>8} {name:36} {t*1e3:9.2f} ms")
    writeCsv("scaling", ["algorithm", "n", "seconds"], rows)
    plt.figure(figsize=(7, 4.5))

    for name in ALGOS:
        xs = [r[1] for r in rows if r[0] == name]; ys = [r[2] / r[1] * 1e9 for r in rows if r[0] == name]
        plt.plot(xs, ys, "o-", label=name)
    plt.xscale("log"); plt.xlabel("n (random integers, k = n/2)"); plt.ylabel("nanoseconds per element")
    plt.title("Time per element vs input size"); plt.legend(); plt.grid(alpha=.3); plt.tight_layout()
    plt.savefig("results/scaling.png", dpi=150); plt.close()

def expFamilies(rng):  # different kinds of input
    n = 2 * 10**4 if QUICK else 2 * 10**5
    rows = []

    for fam, a in families(n, rng).items():
        for name, fn in ALGOS.items():
            t = timeit(fn, a, n // 2, 11)
            rows.append((fam, name, t)); print(f"family {fam:20} {name:36} {t*1e3:9.2f} ms")
    writeCsv("families", ["family", "algorithm", "seconds"], rows)
    fams = list(dict.fromkeys(r[0] for r in rows)); w = 0.27
    plt.figure(figsize=(9, 4.5))

    for i, name in enumerate(ALGOS):
        ys = [next(r[2] for r in rows if r[0] == f and r[1] == name) * 1e3 for f in fams]
        plt.bar([j + (i - 1) * w for j in range(len(fams))], ys, w, label=name)
    plt.xticks(range(len(fams)), fams); plt.ylabel("milliseconds"); plt.title(f"Input families, n = {n}, k = n/2")
    plt.legend(); plt.grid(axis="y", alpha=.3); plt.tight_layout(); plt.savefig("results/families.png", dpi=150); plt.close()

def expTail(rng):  # same input loads of times to see how much the time changes
    n = 10**4 if QUICK else 10**5
    runs = 200 if QUICK else 2000
    a = [rng.randint(0, 10**9) for _ in range(n)]
    data = {}

    for name, fn in list(ALGOS.items())[:2]:  # only the two selection ones
        ts = []

        for _ in range(runs):
            b = list(a); t0 = time.perf_counter(); fn(b, n // 2); ts.append(time.perf_counter() - t0)
        data[name] = ts
        q = statistics.quantiles(ts, n=100)
        print(f"tail {name:36} median {statistics.median(ts)*1e3:.2f} ms  p99 {q[98]*1e3:.2f} ms  max {max(ts)*1e3:.2f} ms")
    writeCsv("tail", ["algorithm", "run", "seconds"], [(nm, i, t) for nm, ts in data.items() for i, t in enumerate(ts)])
    plt.figure(figsize=(7, 4.5))

    for name, ts in data.items():
        plt.hist([t * 1e3 for t in ts], bins=80, alpha=.6, label=name)
    plt.yscale("log"); plt.xlabel("milliseconds"); plt.ylabel("number of runs (log)")
    plt.title(f"Run-time distribution, same input, n = {n}, {runs} runs"); plt.legend(); plt.tight_layout()
    plt.savefig("results/tail.png", dpi=150); plt.close()

def expRank(rng):  # does k change how long it takes
    n = 10**4 if QUICK else 10**5
    a = [rng.randint(0, 10**9) for _ in range(n)]
    ks = [0, n // 100, n // 10, n // 4, n // 2, 3 * n // 4, 9 * n // 10, n - 1]
    rows = []

    for k in ks:
        for name, fn in list(ALGOS.items())[:2]:
            rows.append((name, k, timeit(fn, a, k, 21)))
    writeCsv("rank", ["algorithm", "k", "seconds"], rows)
    plt.figure(figsize=(7, 4.5))

    for name in list(ALGOS)[:2]:
        plt.plot([r[1] / n for r in rows if r[0] == name], [r[2] * 1e3 for r in rows if r[0] == name], "o-", label=name)
    plt.xlabel("k / n"); plt.ylabel("milliseconds"); plt.title(f"Effect of rank k, n = {n}")
    plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.savefig("results/rank.png", dpi=150); plt.close()
    for r in rows: print(f"rank k={r[1]:>6} {r[0]:36} {r[2]*1e3:8.2f} ms")

if __name__ == "__main__":
    for exp in (expScaling, expFamilies, expTail, expRank):
        exp(random.Random(SEED))
    print("Done. See results/")
