"""Interactive helper: tells you what to guess, you tell it the colors
the game showed you, it narrows down the vault code.

Strategy: maximize expected information (Shannon entropy) at each step,
searching the FULL 10,000-code universe as the guess pool (not just
the codes still consistent with feedback so far) for moves 1-3. This
sacrifices the small chance of being correct on a "probe" guess in
exchange for a guess that splits the remaining possibilities more
evenly -- which matters a lot when you only get 4 attempts total. The
4th attempt is always one of the remaining consistent candidates,
since there's no more feedback left to use.

Run with:  python3 -m vaultcracker.cli
Requires:  pip install numpy
"""

import numpy as np

from .fast import ALL_ARR, best_guess, filter_remaining, feedback_batch

MAX_ATTEMPTS = 4
FIRST_GUESS = (0, 1, 2, 3)  # precomputed: highest-entropy opening guess (4.86 bits)

COLOR_INPUT_MAP = {"r": 0, "y": 1, "g": 2}
COLOR_NAMES = {0: "R", 1: "Y", 2: "G"}


def read_feedback():
    while True:
        raw = input("  Colors shown (e.g. rygg, r=red y=yellow g=green): ").strip().lower()
        if len(raw) == 4 and all(c in COLOR_INPUT_MAP for c in raw):
            return tuple(COLOR_INPUT_MAP[c] for c in raw)
        print("  Please enter exactly 4 characters using only r, y, g.")


def code_from_colors(colors):
    code = 0
    for c in colors:
        code = code * 3 + c
    return code


def main():
    remaining = ALL_ARR
    print("Vault Cracker -- up to 4 attempts. I'll suggest each guess.\n")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        if remaining.shape[0] == 1:
            guess = tuple(int(x) for x in remaining[0])
        elif attempt == 1:
            guess = FIRST_GUESS
        elif attempt == MAX_ATTEMPTS:
            guess = tuple(int(x) for x in remaining[0])
        else:
            print(f"  (thinking -- searching {ALL_ARR.shape[0]} possible guesses "
                  f"against {remaining.shape[0]} remaining codes...)")
            guess, score = best_guess(remaining, ALL_ARR)

        print(f"Attempt {attempt}: guess {''.join(map(str, guess))}")
        if remaining.shape[0] == 1:
            print("(This is the only code left that fits -- it should be it.)")

        colors = read_feedback()
        print(f"  -> {''.join(COLOR_NAMES[c] for c in colors)}")

        if colors == (2, 2, 2, 2):
            print(f"\nCracked it in {attempt} attempt(s): {''.join(map(str, guess))}")
            return

        code = code_from_colors(colors)
        remaining = filter_remaining(remaining, guess, code)

        if remaining.shape[0] == 0:
            print("\nNo codes match that feedback -- double check what you entered.")
            return

        print(f"  {remaining.shape[0]} possible code(s) remain.\n")

    print("\nOut of attempts.")
    if remaining.shape[0]:
        sample = [''.join(map(str, c)) for c in remaining[:10].tolist()]
        print(f"Remaining candidates (up to 10 shown): {sample}")


if __name__ == "__main__":
    main()
