# Run brief: the hourly run (2026-11-10)

**Purpose.** On the default data (BTC, plus ETH for the RSI ideas, daily bars, fold A), the 13 testable ideas all came out inconclusive, every |t| below 1.4 (`05_verification/verdicts/REVIEW.md`). The chain works; the data could not decide. This run asks whether more bars can: the same two theories, with hourly bars.

**Approved scope (operator, 2026-11-10).** Briefs 001 (RSI extremes) and 002 (moving-average cross), with `bar: 1h` added to their headers, through steps 2 to 5 with the current helpers. Fold A. Step 5 runs twice side by side. No trial ledger.

**Pre-registered outcomes.**
- **A.** Some plan reaches |t| ≥ 2 (confirmed or rejected): data size was the bottleneck. Next: reconsider the default bar size.
- **B.** All inconclusive again, with about 24 times more bars: these ideas show no effect at this scale. Next: back to the briefs and ideas (steps 1 and 2), not more data.
- **C.** A chain defect (a mismatch, an engine refusal, or a status that differs between the two runs): fix it first.

**Where the outputs go.** `hourly_run/` in each step folder: `01_brief/hourly_run/briefs/`, `02_ideation/hourly_run/ideas/`, `03_test_plan/hourly_run/plans/`, `04_backtest/hourly_run/backtests/`, `05_verification/hourly_run/verdicts/` (and `verdicts_run2/`).

**Result.** To be written after the run: which outcome happened.
