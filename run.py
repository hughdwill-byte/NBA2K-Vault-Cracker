#!/usr/bin/env python3
"""Single entry point for the vault code solver.

Run with:  python3 run.py
"""

import sys


def main():
    print("Vault Cracker\n")
    print("1) Solve a real vault code (enter the colors you see in-game)")
    print("2) Practice mode (program picks a hidden code, you try to crack it)")
    choice = input("\nChoose 1 or 2: ").strip()

    if choice == "2":
        from vaultcracker import mock
        mock.main()
    else:
        from vaultcracker import cli
        cli.main()


if __name__ == "__main__":
    sys.exit(main())
