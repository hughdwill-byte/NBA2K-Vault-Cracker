# NBA2K Vault Cracker

A solver for the NBA2K 4-digit vault code mini-game. The code is four digits from 0–9, and repeats are allowed. You get 4 attempts, and each attempt gives red/yellow/green feedback per digit:

- 🟩 **Green**: right digit, right position
- 🟨 **Yellow**: right digit, wrong position
- 🟥 **Red**: the digit isn't in the code

## How it works

There are 10,000 possible codes and only 4 guesses, and the 4th guess gets no feedback you can still act on. So for guesses 1–3, the solver picks whichever code maximises the Shannon entropy of the feedback. It searches the full 10,000-code universe, not just the codes that could still be correct. These "probe" guesses often can't be the answer themselves, but they split the remaining possibilities much more evenly. Guess 4 is always a code that is still consistent with the feedback.

This roughly doubles the success rate within 4 attempts: about 68–73%, compared with about 46% when only consistent codes are guessed. The best opening guess is precomputed as `0123` (4.86 bits).

## Usage

Requires Python 3.9+ and NumPy.

```bash
pip install -r requirements.txt
python3 run.py
```

`run.py` offers two modes:

1. **Solve**: use this while playing. The solver suggests a guess, and you type the colours the game showed you (e.g. `rygg`).
2. **Practice**: the program hides a random code for you to crack. Type `hint` to see what the solver would play.

### Measure the success rate

```bash
python3 -m vaultcracker.simulate_fast 500 full        # probe guesses from the full universe
python3 -m vaultcracker.simulate_fast 500 remaining   # baseline: consistent codes only
```

Prints a histogram of the attempt each code was solved on, plus the overall success rate.

## Project layout

| File | Purpose |
|---|---|
| `run.py` | Entry point: choose solve or practice mode |
| `vaultcracker/cli.py` | Interactive solver for real games |
| `vaultcracker/mock.py` | Practice mode with a hidden random code and hints |
| `vaultcracker/feedback.py` | Feedback scoring rules |
| `vaultcracker/fast.py` | Vectorised (NumPy) feedback and entropy calculations |
| `vaultcracker/simulate_fast.py` | Monte Carlo benchmark of the strategy |
