"""Practice mode: the program picks a random hidden passkey and lets
you try to crack it yourself, no real NBA2K vault needed.

Rules match the real game: 4 digits, 0-9, repeats allowed, 4 attempts,
red/yellow/green feedback per position.

Type a 4-digit guess each round. Type `hint` instead of a guess to see
what the entropy-maximizing solver would play next.

Run with:  python3 -m vaultcracker.mock
"""

import random

from .fast import ALL_ARR, best_guess, filter_remaining, feedback_batch
import numpy as np

MAX_ATTEMPTS = 4
FIRST_GUESS = (0, 1, 2, 3)
COLOR_NAMES = {0: "R", 1: "Y", 2: "G"}


def read_guess():
    while True:
        raw = input("  Your guess (4 digits, 0-9, or 'hint'): ").strip().lower()
        if raw == "hint":
            return None
        if len(raw) == 4 and raw.isdigit():
            return tuple(int(ch) for ch in raw)
        print("  Enter exactly 4 digits (0-9), or 'hint'.")


def main():
    secret = tuple(random.randint(0, 9) for _ in range(4))
    remaining = ALL_ARR

    print("Mock Vault -- I've picked a secret 4-digit code (0-9, repeats allowed).")
    print(f"You have {MAX_ATTEMPTS} attempts. Type 'hint' anytime for the solver's suggestion.\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"Attempt {attempt}/{MAX_ATTEMPTS} -- {remaining.shape[0]} code(s) still possible.")
        guess = read_guess()

        while guess is None:
            if remaining.shape[0] == 1:
                suggestion = tuple(int(x) for x in remaining[0])
            elif attempt == 1 and remaining.shape[0] == ALL_ARR.shape[0]:
                suggestion = FIRST_GUESS
            else:
                pool = ALL_ARR if attempt < MAX_ATTEMPTS else remaining
                suggestion, _ = best_guess(remaining, pool)
            print(f"  Hint: try {''.join(map(str, suggestion))}")
            guess = read_guess()

        code = int(feedback_batch(guess, np.array([secret]))[0])
        digits = []
        c = code
        for _ in range(4):
            digits.append(c % 3)
            c //= 3
        digits.reverse()
        colors = "".join(COLOR_NAMES[d] for d in digits)
        print(f"  -> {colors}")

        if guess == secret:
            print(f"\nCracked it in {attempt} attempt(s)! The code was {''.join(map(str, secret))}.")
            return

        remaining = filter_remaining(remaining, guess, code)
        print()

    print(f"Out of attempts. The code was {''.join(map(str, secret))}.")


if __name__ == "__main__":
    main()
