# Run brief: the full-data run (2026-11-11)

**Purpose.** Every verdict so far is inconclusive (13 daily, 10 hourly). A planted-effect test (`05_verification/planted_test/`) shows step 5 does confirm and reject when an effect is there, so this is not a bug of step 5. It also shows the tests' reach: on fold A, 002-05 needs about +0.4 % a day (about +150 % a year) to reach t = 2. For an edge of steady size, t grows with the square root of the years covered, not with the number of bars, which is why hourly bars did not help. The data was 2 years and 1 or 2 coins. This run asks: with about 8 years and 6 coins, does an idea come out confirmed or rejected?

**Scope (fixed before any data of folds B to D is seen).**
- Brief 002 (moving-average cross, trend persistence), the theory with the strongest outside support (time-series momentum), and the one whose text names no coin, so the coins can be widened without changing the theory.
- Coins: the six cached Kraken coins with full data in all four folds: BTC, ETH, LTC, XMR, XRP, ZEC. Chosen on data coverage only.
- Period: folds A, B, C, D (24 windows, about 8 years; walk-forward folds only, never the holdout). Daily bars.
- Steps 2 to 5 with the current helpers (step 3 with the two approved fixes and the fidelity line). Step 4 now accepts several folds (a small change: the windows of the folds, one after the other). Step 5 runs twice side by side.
- The thresholds are not changed: confirm and reject at |t| ≥ 2, as the plans state.

**Pre-registered outcomes.**
- **A.** At least one plan is confirmed or rejected, the same in both runs: the inconclusive verdicts came from too little data. Next: the default data becomes all folds and the coins with full data.
- **B.** All inconclusive, with about 24 times the evidence: trend persistence shows no effect large enough to see, even on 8 years and 6 coins. Next: the conclusion leans to "these textbook ideas are not real here"; look at whether the criteria's comparison dilutes the effect (see the planted test's reading).
- **C.** A chain defect (a mismatch, an engine refusal, a status that differs between the runs): fix it first.

**A caution fixed now.** Six plans, about four distinct forecasts: a t of 2 on one of them can happen by chance (roughly one chance in five). A confirm will be read with the per-fold results beside it (described, not used to change the verdict).

**Result.** To be written after the run.
