"""Numpy-accelerated simulation that searches the FULL 10,000-code
universe as the guess pool on moves 1-3 (not just the shrinking
candidate set), to see whether "probe" guesses that can't be the
answer themselves but split the space more evenly actually improve
the odds of cracking the code within 4 attempts.
"""

import random
import sys
import time
from collections import Counter

import numpy as np

from .fast import ALL_ARR, best_guess, filter_remaining, feedback_batch

MAX_ATTEMPTS = 4
FIRST_GUESS = (0, 1, 2, 3)  # precomputed: highest-entropy move 1 (4.8585 bits)


def play(secret, full_universe_pool=True):
    remaining = ALL_ARR
    secret_arr = np.array([secret])

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if remaining.shape[0] == 1:
            guess = tuple(int(x) for x in remaining[0])
        elif attempt == 1:
            guess = FIRST_GUESS
        elif attempt == MAX_ATTEMPTS:
            guess = tuple(int(x) for x in remaining[0])
        else:
            pool = ALL_ARR if full_universe_pool else remaining
            guess, _ = best_guess(remaining, pool)

        if guess == secret:
            return attempt

        code = int(feedback_batch(guess, secret_arr)[0])
        remaining = filter_remaining(remaining, guess, code)
        if remaining.shape[0] == 0:
            raise RuntimeError("filtering bug: no candidates left")

    return None


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    mode = sys.argv[2] if len(sys.argv) > 2 else "full"
    full_universe_pool = mode == "full"

    random.seed(0)
    secrets = random.sample(list(map(tuple, ALL_ARR.tolist())), n)

    start = time.time()
    results = [play(s, full_universe_pool) for s in secrets]
    elapsed = time.time() - start

    histogram = Counter(results)
    solved = sum(v for k, v in histogram.items() if k is not None)

    print(f"mode={'full-universe probes' if full_universe_pool else 'remaining-only'} "
          f"n={n} time={elapsed:.1f}s ({elapsed/n*1000:.0f} ms/secret)\n")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        cnt = histogram.get(attempt, 0)
        print(f"  Solved on attempt {attempt}: {cnt:4d}  ({cnt/n:.1%})")
    failed = histogram.get(None, 0)
    print(f"  Not solved within {MAX_ATTEMPTS}: {failed:4d}  ({failed/n:.1%})")
    print(f"\nOverall success rate within {MAX_ATTEMPTS} attempts: {solved/n:.1%}")


if __name__ == "__main__":
    main()
