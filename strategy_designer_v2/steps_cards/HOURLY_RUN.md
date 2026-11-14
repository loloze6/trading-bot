# Run brief: the hourly run (2026-11-10)

**Purpose.** On the default data (BTC, plus ETH for the RSI ideas, daily bars, fold A), the 13 testable ideas all came out inconclusive, every |t| below 1.4 (`05_verification/verdicts/REVIEW.md`). The chain works; the data could not decide. This run asks whether more bars can: the same two theories, with hourly bars.

**Approved scope (operator, 2026-11-10).** Briefs 001 (RSI extremes) and 002 (moving-average cross), with `bar: 1h` added to their headers, through steps 2 to 5 with the current helpers. Fold A. Step 5 runs twice side by side. No trial ledger.

**Pre-registered outcomes.**
- **A.** Some plan reaches |t| ≥ 2 (confirmed or rejected): data size was the bottleneck. Next: reconsider the default bar size.
- **B.** All inconclusive again, with about 24 times more bars: these ideas show no effect at this scale. Next: back to the briefs and ideas (steps 1 and 2), not more data.
- **C.** A chain defect (a mismatch, an engine refusal, or a status that differs between the two runs): fix it first.

**Where the outputs go.** `hourly_run/` in each step folder: `01_brief/hourly_run/briefs/`, `02_ideation/hourly_run/ideas/`, `03_test_plan/hourly_run/plans/`, `04_backtest/hourly_run/backtests/`, `05_verification/hourly_run/verdicts/` (and `verdicts_run2/`).

## Review (2026-11-10)

**Runs read:** this run (steps 2 to 5, verdicts twice). **PRs merged:** 0. **Blocks in the registry:** none added by this work.

**Outcome B happened.** 10 of 10 plans are inconclusive, the same status in both runs. Every situation check is 1.0, and the largest |t| is 1.23. The samples are large now: for example, 390 to 782 pooled non-overlapping extreme cases for the RSI ideas, and 340 to 384 non-overlapping 24-bar blocks for the cross ideas. On BTC (and ETH) over fold A, these two theories show no effect, either way, at 1h or at 1d.

**The books, before the tables.**
- **The RSI books are active on 50 % of the bars.** "RSI at a high extreme" was adapted to "graded in RSI's distance above 50", so a position is held whenever RSI is above 50. About 600 trades per window; summed over the six windows, the books lose 1.4 to 3.0, against +0.44 (BTC) and -0.11 (ETH) for holding. The loss is turnover. The verdicts are unaffected: their criteria measure the top decile, before costs. But an "extreme" idea held half the time is not a book a trader would run. The one change a practitioner would make: hold a position only at the extreme.
- **The cross books come in identical pairs.** 002-01 equals 002-05 (+0.76), and 002-02 equals 002-06 (+0.35): after the cross and while in the zone become the same forecast (parked item). Six plans gave four distinct tests.

**Defects the run showed.**
- **A "no difference" reject.** 001-02's plan rejected on |t| below 2, twice (first plan, and its one rerun, with a ±0.1 % band and no interval). It did not decide the verdict (the estimate, -0.13 %, is outside the band). It is the second case after daily 002-03. The cause is in the briefs themselves: 001 says the theory is wrong if behaviour "looks the same" after extremes. Symmetric criteria give no proper way to reject on "no difference".
- **Value and t from different samples** (002-01: the value over all active bars, the t over non-overlapping blocks). Both near zero; no status depends on it.

**Cost.** About 2.45 USD (ideas 0.07, plans 0.63, verdicts 0.97 and 0.78). Backtests about 45 minutes.

## Decision set proposed (not approved)

1. **Per outcome B: back to steps 1 and 2, not more data.** The ideas the vessel can test today are textbook single-coin signals, and they show nothing at either bar size. The ideas with a structural reason (bitcoin leads altcoins, 7 ideas) are untestable in a one-coin config; the divergence ideas wait for components. The question for the roadmap is which of these to open: a two-coin vessel, the wish-list components, or new briefs.
2. **Step 3, "no difference" rejects:** allow one only as an equivalence test, fixed in the plan: the whole confidence interval (say 90 %) inside a stated band. Otherwise it is inconclusive. A prompt line, tested by two exercises.
3. **Step 3, extremes:** an "extreme" situation adapted to a graded forecast should carry near-zero position away from the extreme (a convex transform strong enough, or a threshold component if the catalogue has one). Needs a look at what the catalogue allows before a rule.
4. **Not now:** costs and turnover belong to step 6.
