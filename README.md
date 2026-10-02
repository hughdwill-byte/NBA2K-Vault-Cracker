# 🏀 NBA2K Vault Cracker

A solver for NBA 2K's **4-digit vault code** mini-game. You get **4 attempts** to guess a
4-digit code (each digit `0–9`, repeats allowed → **10,000** possible codes). After each
guess the game colours every position:

- 🟢 **green** — right digit, right spot
- 🟡 **yellow** — right digit, wrong spot
- 🔴 **red** — digit not in the code at all

Enter those colours and the solver tells you the strongest next guess.

## Use it

```bash
pip install -r requirements.txt     # just numpy
python3 run.py
```

`run.py` offers two modes:

1. **Solve a real vault code** — it suggests each guess; you type the colours the game
   showed (e.g. `gyrr`) and it narrows the code down.
2. **Practice mode** — the program hides a code and you try to crack it, to test the
   strategy yourself.

Prefer to jump straight in? The two modes are also directly runnable:

```bash
python3 -m vaultcracker.cli     # solve a real code
python3 -m vaultcracker.mock    # practice against a hidden code
```

## How it works

With 10,000 possible codes and only 4 guesses — the last of which can't use any new
feedback — guessing only codes that *could still be correct* is weak. Instead, for moves
1–3 the solver maximises the **Shannon entropy** of each guess's colour outcome against the
**full 10,000-code universe**, not just the shrinking candidate set. Spending early guesses
as pure information-gathering **"probes"** (which often can't be the answer themselves)
splits the remaining possibilities far more evenly, so by the final attempt far fewer
candidates remain. The 4th guess is always one of the still-consistent codes, since there's
no feedback left to exploit. The opening guess is precomputed as `0 1 2 3` (≈4.86 bits).

### Does the probe strategy actually help?

Yes — measurably. `vaultcracker/simulate_fast.py` plays the solver against random secret
codes in both modes:

```bash
python3 -m vaultcracker.simulate_fast 300 full        # entropy probes over the full universe
python3 -m vaultcracker.simulate_fast 300 remaining   # baseline: guess only still-possible codes
```

Measured success rate within 4 attempts (seed-fixed sample):

| Strategy | Success within 4 attempts |
|---|---|
| **Full-universe entropy probes** | **≈66%** |
| Remaining-candidates only (baseline) | ≈42% |

So the probe strategy **roughly doubles** the real-world crack rate. (The full-universe
search is heavier — a few seconds per code — because every move is scored against all
10,000 codes.)

## Repo layout

| File | Purpose |
|---|---|
| `run.py` | Single entry point — menu for solve vs. practice mode |
| `vaultcracker/cli.py` | Interactive solver — use this while playing |
| `vaultcracker/mock.py` | Practice mode: the program hides a code you try to crack |
| `vaultcracker/feedback.py` | Feedback (red/yellow/green) scoring logic |
| `vaultcracker/fast.py` | NumPy-accelerated entropy / best-guess computations |
| `vaultcracker/simulate_fast.py` | Monte-Carlo simulation to measure success rate |

## Requirements

Python 3.8+ and NumPy (`pip install -r requirements.txt`).
