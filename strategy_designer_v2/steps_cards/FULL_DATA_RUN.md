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

## Review (2026-11-11)

**Runs read:** this run (steps 2 to 5, verdicts twice); the planted test. **PRs merged:** 0. **Blocks in the registry:** none added by this work.

**What came out.** 6 ideas, 6 plans. Backtests: 141 of 144 coin-windows per plan (the engine refused 1 XMR and 2 XRP windows: not enough daily history before them for the 200-day average; a data gap, not a config fault). Verdicts, the same status in both runs: **5 rejected** (t from -2.6 to -4.6), 1 inconclusive (002-05). Every situation check passed. Cost: 0.04 (ideas) + 0.34 (plans) + 0.57 and 0.64 (verdicts) USD; backtests about 25 minutes.

**Formally, outcome A happened: with more data, the chain decides. But the five rejections are not about the market. They are a flaw of the measure.**

**The books first.** Over the 8 years, the long trend books (002-01, 002-03) beat holding on BTC and ETH and lose to it on XMR, XRP, ZEC and LTC; the short books lose almost everywhere (`05_verification/full_data_run/diagnosis/baseline_compare_output.txt`). Nothing there looks like a strong, steady reversal after crosses, which is what five strong rejections would mean.

**The flaw.** Every plan judges the idea "against simply holding the coin", as the step 3 prompt asks, and every plan realises it as the coin's mean return **over the same window**. That mean includes the very price moves that switched the slow trend signal on. When the 50/200 signal is on, the window's mean is high for that reason, so the "excess" is pushed below zero, whatever the market does next.
- **Proof on random walks** (`diagnosis/random_walk_check.py`), where no effect exists: the same measure gives t = -2.60 on average (-3.56 to -1.80 over 20 simulated datasets). A trend idea is "rejected" out of nothing.
- **On the record**, against the coin's mean over all its windows instead of the same window: 002-01 goes from t -2.91 to +0.09, 002-03 from -2.86 to +0.61, 002-02 from -3.51 to +0.11. In-position minus flat, raw: +0.08 %, +0.71 %, -0.08 % per 10 bars.
- **It was always there.** Every plan since the start uses a per-window mean. On fold A the noise hid it (all inconclusive); with 8 years and 6 coins it turned "no effect" into five rejections. It biases against trend-type ideas and towards reversal-type ideas.

## The conclusion of the investigation ("why is no idea ever proven?")

1. **Not a bug of step 5.** The planted test: step 5 confirms (t 5.5) and rejects (t -4.1) planted effects, in the right direction (`05_verification/planted_test/reading.md`).
2. **Not a threshold too strict.** t of 2 is the usual bar. It is not the cause.
3. **The sample was too small.** On fold A (2 years, 1 or 2 coins), t = 2 needs an annual Sharpe of about 1.4 before costs; a strong realistic edge (+0.1 %/day) stays inconclusive. For an edge of steady size, t grows with the square root of the years, not with the number of bars: hourly bars could not help.
4. **A real flaw of the measure: the "holding" reference taken over the same window.** It hid under small samples and shows with large ones. It is a step 3 matter (how a plan states its reference); step 5 applied it faithfully.
5. **With the flaw removed, trend persistence on these 6 coins over 8 years shows no effect** (t between +0.09 and +0.61). This textbook idea is not real here, at this scale, before costs. So no proven idea yet, for two reasons: the sample before, the measure now; and the ideas tested so far are textbook signals.

**These verdicts must not be used.** They are kept in git (commit `5fb1516`) as the record of the flaw; the folder now holds the rerun below.

## Decision set proposed (not approved, nothing built)

1. **Step 3, the reference.** One general line: "Against holding: the coin's mean return over all the test's windows, never a mean taken over the same window: such a mean shares the bars that set the forecast." (Or: compare the bars with a position against the bars without one.) Tested by two exercises, then this run's plans rewritten; steps 4 (no rerun: the configs do not change) and 5 rerun.
2. **The default data:** all four folds and the coins with full data, so that a realistic edge can show. Steps 3 and 4 already accept several folds: the one change made tonight that you have not approved (a few lines; "fold A" records are untouched). Keep or revert.
3. **Then new ideas.** With a sound measure and enough data, the briefs worth testing are those with a reason beyond a textbook signal (the two-coin ideas, the wish-list components).

## Rerun with the fixed reference (2026-11-11, approved: "Go")

Step 3 now says: holding is the coin's mean over all the test's windows, never over a single window (exercises 27 and 28). The 6 plans were rewritten; their configs did not change, so step 4 kept every record; step 5 ran twice side by side. Cost: 0.31 (plans) + 0.53 and 0.64 (verdicts) USD.

| Plan | Run 1 | Run 2 |
|---|---|---|
| 002-01 after an up-cross | inconclusive, t 0.37 | inconclusive, t 0.41 |
| 002-02 after a down-cross | inconclusive, t 0.39 | inconclusive, t 0.26 |
| 002-03 price above its long average | inconclusive, t 1.25 | inconclusive, t 1.25 |
| 002-04 price below its long average | inconclusive, t -0.27 | inconclusive, t -0.27 |
| 002-05 up-cross to down-cross | inconclusive, t -0.04 | inconclusive, t -0.04 |
| 002-06 down-cross to up-cross | inconclusive, t 0.12 | inconclusive, t 0.12 |

The same status in both runs; every situation check 1.0. It matches the diagnosis (t +0.09 to +0.61 against the all-window mean). **On 6 coins over about 8 years, trend persistence after moving-average crosses shows no effect, before costs.** This time the sample was large enough to see a realistic edge (t = 2 needs an annual Sharpe of about 0.7 over 8 years), so the "inconclusive" is informative: if the effect exists here, it is small.
