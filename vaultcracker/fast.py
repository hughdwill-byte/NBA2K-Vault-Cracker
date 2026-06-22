"""Numpy-vectorized feedback + entropy search, used to evaluate guess
strategies fast enough to brute-force the FULL 10,000-code universe as
the guess pool on every move (not just the shrinking candidate set).
"""

import itertools
import math

import numpy as np

ALL_CODES = list(itertools.product(range(10), repeat=4))
ALL_ARR = np.array(ALL_CODES, dtype=np.int16)  # (10000, 4)


def feedback_batch(guess, secrets_arr):
    """guess: tuple[int,int,int,int]. secrets_arr: (N,4) int array.
    Returns (N,) array of feedback codes in base-3 (0=R,1=Y,2=G per digit)."""
    n = secrets_arr.shape[0]
    guess_arr = np.asarray(guess, dtype=np.int16)
    colors = np.zeros((n, 4), dtype=np.int8)
    counts = np.zeros((n, 10), dtype=np.int16)
    for d in range(10):
        counts[:, d] = np.sum(secrets_arr == d, axis=1)

    green_mask = secrets_arr == guess_arr[None, :]
    colors[green_mask] = 2
    for i in range(4):
        gi = int(guess_arr[i])
        gm_i = green_mask[:, i]
        counts[gm_i, gi] -= 1

    for i in range(4):
        gi = int(guess_arr[i])
        not_green = ~green_mask[:, i]
        has_rem = counts[:, gi] > 0
        is_yellow = not_green & has_rem
        colors[is_yellow, i] = 1
        counts[is_yellow, gi] -= 1

    return colors[:, 0] * 27 + colors[:, 1] * 9 + colors[:, 2] * 3 + colors[:, 3]


def entropy_of_guess(guess, remaining_arr):
    codes = feedback_batch(guess, remaining_arr)
    n = remaining_arr.shape[0]
    counts = np.bincount(codes, minlength=81).astype(np.float64)
    counts = counts[counts > 0]
    p = counts / n
    return float(-np.sum(p * np.log2(p)))


def best_guess(remaining_arr, guess_pool_arr):
    """Returns (guess_tuple, entropy_bits) maximizing expected information
    against `remaining_arr`, searching over every row of `guess_pool_arr`."""
    best_idx, best_score = -1, -1.0
    remaining_set = {tuple(r) for r in remaining_arr.tolist()}
    for idx in range(guess_pool_arr.shape[0]):
        guess = tuple(int(x) for x in guess_pool_arr[idx])
        score = entropy_of_guess(guess, remaining_arr)
        if score > best_score + 1e-9:
            best_idx, best_score = idx, score
        elif abs(score - best_score) <= 1e-9 and guess in remaining_set:
            # tie-break: prefer a guess that could itself be the answer
            if tuple(int(x) for x in guess_pool_arr[best_idx]) not in remaining_set:
                best_idx, best_score = idx, score
    guess = tuple(int(x) for x in guess_pool_arr[best_idx])
    return guess, best_score


def filter_remaining(remaining_arr, guess, code):
    codes = feedback_batch(guess, remaining_arr)
    return remaining_arr[codes == code]
