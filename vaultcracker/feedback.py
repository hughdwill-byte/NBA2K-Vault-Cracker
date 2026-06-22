"""Feedback computation for the 4-digit vault code game.

Colors are encoded as small ints: 0 = RED, 1 = YELLOW, 2 = GREEN.
"""

from collections import Counter

RED, YELLOW, GREEN = 0, 1, 2
COLOR_NAMES = {RED: "R", YELLOW: "Y", GREEN: "G"}


def get_feedback(guess, secret):
    """Return a tuple of 4 colors for `guess` against `secret`.

    Duplicate digits are handled the same way Wordle handles duplicate
    letters: exact-position matches are claimed first, then any
    leftover copies of a digit in the secret are handed out to the
    guess's remaining occurrences of that digit, left to right.
    """
    colors = [RED, RED, RED, RED]
    remaining = Counter(secret)

    # Pass 1: greens claim their digit first.
    for i in range(4):
        if guess[i] == secret[i]:
            colors[i] = GREEN
            remaining[guess[i]] -= 1

    # Pass 2: yellows claim leftover copies, left to right.
    for i in range(4):
        if colors[i] == GREEN:
            continue
        d = guess[i]
        if remaining[d] > 0:
            colors[i] = YELLOW
            remaining[d] -= 1
        # else stays RED

    return tuple(colors)


def encode(colors):
    """Pack a 4-color feedback tuple into a single base-3 int (0..80)."""
    code = 0
    for c in colors:
        code = code * 3 + c
    return code


def format_feedback(colors):
    return "".join(COLOR_NAMES[c] for c in colors)
