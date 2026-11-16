# Exercise 3: step 6 as a profitability check of the backtest

**Change.** Step 6 is now only "is this backtest's book profitable enough?". Its input is one backtest record: it no longer reads the idea's verdict, the plan or its fit. The script is `helper/check_profitability.py`, its output a "check" (`check.md`, `result.json`) in `checks/`. The calculation and the rule are unchanged.

**Run.** (Rerun after removing "the book in figures", which no rule reads: approved.) The 16 real records of exercises 1 and 2 (full-data run, 6; hourly run, 10). No warning, no error. The tests pass (4 of 4).

- **16 of 16 checks are identical to exercise 2:** the same status, the same six values, the same figures.
- **Every book is "not profitable enough".** The closest is 002-03 hourly (BTC), which fails on Calmar alone (0.63 against 0.75).

**Status.** "Done when" is met.
