# Exercise 2: branch 3 on every backtest

**Change** (approved: "remove the gate"). Branch 3 assesses every backtest, whatever branch 1 said, and copies branch 1's verdict next to its result. The `--any-verdict` option is gone. The status reads "profitable enough" or "not profitable enough". The folder is renamed `06_profitability`.

**Run.** The same 16 real records as exercise 1 (full-data run, 6; hourly run, 10). No warning, no error.

- **Every number is identical to exercise 1** (`result.json`, compared field by field, branch 1's verdict aside).
- **Every book is "not profitable enough"**, and its index line shows "(idea: inconclusive)".
- The tests still pass (4 of 4).

**Status.** "Done when" is met.
