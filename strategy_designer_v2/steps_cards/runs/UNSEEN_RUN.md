# Unseen run: do the paying ideas still pay on dates the research never saw? (plan, 2026-11-18)

## Business objective
Before any money or paper trading: the ideas steps 5 and 6 passed were found and judged on the same years
(2018 to 2025). Picked from 174 verdicts, some may have passed by luck. Dates the research never touched tell which.

**Never seen** = a date outside every fold's window (folds A to D cover 2018-01-01 to 2025-12-31) and outside any bar a
step read. Two such periods exist with usable daily bars:

| Period | Coins | Bars | Source | Note |
|---|---|---|---|---|
| **2026** (Jan 1 to Nov 17) | the 19 Kraken coins | about 320 a coin | Kraken's public daily API (gives back to 2024-11-28, so the warm-up is covered) | includes the policy's 2026 H1 holdout: this run uses it; recorded in `holdout_consumed_by` |
| **2016 to 2017** | BTC, ETH, LTC (XMR, XRP, ZEC from 2017) | 730 a coin | already in `local_data/` | 2014 to 2015 left out: too thin (median 9 to 73 trades a day, LTC 64 days with no move in 2014) |

Not used: the recorder (book and trades since 2026-07-26, not bars; the API gives the bars); forward paper trading
(months; it comes after this, for what passes).

## The candidates, frozen now
The 12 ideas step 5 confirmed and step 6 found profitable enough, every run (one rule, no picking). Configs, coins,
costs and plans unchanged; no step 3 rerun, no tuning.

| Run | Idea (short) | Coins |
|---|---|---|
| night_005 | volatile-day reversal completes quickly | 2 |
| night_006 | volatility-scaled momentum continuation | 6 |
| night_013 | rising-month weekly momentum | 6 |
| night_013 | nearness to high, more coins | 18 |
| night_013 | momentum continuation in uptrends | 6 |
| night_rsi | RSI side predicts next week | 2 |
| validation | high-RSI trend continuation | 6 |
| validation | high-RSI uptrend continuation | 6 |
| validation | momentum inside golden-cross uptrends | 15 |
| validation | short-horizon uptrend momentum near highs | 6 |
| validation | short-horizon dual momentum | 6 |
| volume | heavy-volume rising follow-through | 6 |

## How each is judged (the same rules as in-sample)
- Step 4 backtests each idea on each period, windows of 4 months like the folds (2026: 3 windows, the last ending
  Nov 17; 2016 to 2017: 6 windows).
- Step 5 applies each plan's own criterion unchanged (t ≥ 2 confirms). Step 6 its bars unchanged.
- **Power, said plainly:** in-sample each idea had 24 windows (8 years); the two periods together are about 2.9 years,
  fewer coins in 2016 to 2017. An idea exactly as strong as in-sample would reach t ≈ 1.3 to 1.8, not 2. So a "not
  confirmed" is expected even for a real idea, and is not a failure by itself.
- So one more read, fixed now: **holds** = the main measure has its in-sample sign AND the book's Sharpe after costs
  > 0, on that period. Buy-and-hold on the same coins and dates is shown next to each (2026's direction matters).

## Outcomes, written before the run
| Outcome | Count | Means | Next |
|---|---|---|---|
| 1. The family holds | ≥ 8 of 12 hold on 2026 AND ≥ 8 of 12 on 2016 to 2017 | the trend edge is real out of sample | paper trading via the live session, starting with the ideas that hold on both |
| 2. Depends on the period | holds on one period, not the other | the edge exists in some markets | the regime line: when to switch it on |
| 3. Mostly luck | ≤ 4 of 12 hold on 2026 | selection fit the 2018 to 2025 years | stricter step 5 and 6 bars before more ideas; no paper trading |
| between | 5 to 7 | unclear | named per idea; the operator decides |

The 12 are not 12 independent tries (10 are trend following): the count is read as one family, plus the reversal
(night_005) on its own.

## Why this can't leak
Only closed daily bars (the API's current, unfinished day is dropped: the last bar is 2026-11-17). The engine hands
each bar's decision the rows up to that bar. The new bars go in a separate folder; the cached files are not changed.

## Effort, cost, risk
- **Build** (about 2 hours): a fetch script (19 coins, one call each); the two periods as windows step 4 can run; a
  check that the API's bars equal the cached ones where they overlap (2024-11-28 to 2025-12-31) before using them.
- **Run:** 12 ideas × 2 periods, about an hour; no model call expected (steps 5 and 6 compute with code), under 5 USD.
- **Risks:** the wrapper refuses windows in the holdout range today (a change to shared code: `trading-bot/backtest/`;
  proven by a fixed backtest rerun, files identical); once read, 2026 is no longer unseen for later ideas (the
  recorder's bars after today will be the next unseen period).

## Reading (2026-11-18, run 09:14 to 09:41 UTC, 0 USD)
Ran as planned: 12 ideas × 2 periods, every coin with data ran (BNB has none on Kraken, as in-sample; XMR, XRP and ZEC
start in 2017). Step 5 applied each idea's own saved `measure.py` (no model call); step 6 its bars. Records:
`04_backtest/unseen_run/`, `05_verification/unseen_run/`, `06_profitability/unseen_run/` (per period).

| Idea (run) | In-sample t / Sharpe | 2026: t / Sharpe (holding) / step 6 | 2016-17: t / Sharpe (holding) / step 6 | Holds |
|---|---|---|---|---|
| volatile-day reversal (night_005) | +3.50 / 1.16 | −1.91 / −0.58 (−0.62) / no | +0.55 / −0.46 (3.71) / no | neither |
| volatility-scaled momentum (night_006) | +3.00 / 0.97 | +0.23 / 0.40 (0.10) / no | +1.28 / 2.98 (3.75) / no | both |
| rising-month weekly momentum (night_013) | +3.47 / 0.97 | −1.78 / 0.74 (0.10) / no | +0.25 / 2.95 (3.75) / no | 2016-17 only |
| nearness to high, 19 coins (night_013) | +3.77 / 1.25 | +0.92 / 1.00 (0.07) / no | +0.82 / 2.97 (3.19) / no | both |
| momentum in uptrends (night_013) | +2.79 / 1.15 | +0.52 / 1.34 (0.10) / **yes** | **+2.76** / 3.05 (3.75) / no | both |
| RSI side, next week (night_rsi) | +2.93 / 1.03 | +1.15 / 1.76 (−0.62) / **yes** | +2.25 / 3.17 (3.71) / no | both |
| high-RSI trend continuation (validation) | +3.48 / 1.02 | +3.36 / 1.26 (0.10) / **yes** | **+2.16** / 3.54 (3.75) / no | both |
| high-RSI uptrend continuation (validation) | +3.17 / 1.05 | +2.59 / 1.52 (0.10) / **yes** | **+2.77** / 3.63 (3.75) / no | both |
| momentum in golden-cross uptrends (validation) | +4.61 / 0.90 | +1.67 / 0.76 (−0.07) / no | +0.68 / 2.51 (3.12) / no | both |
| uptrend momentum near highs (validation) | +2.20 / 0.95 | +1.56 / 1.65 (0.10) / **yes** | +1.77 / 3.03 (3.07) / no | both |
| dual momentum (validation) | +2.22 / 1.06 | +1.12 / 1.49 (0.10) / **yes** | +1.37 / 3.31 (3.78) / no | both |
| heavy-volume follow-through (volume) | +2.75 / 0.91 | **+2.30** / 0.45 (0.10) / no | +1.47 / 2.75 (3.75) / no | both |

(Bold t: confirmed by the plan's own criterion. Some t ≥ 2 read "not observable": fewer cases than the plan's
minimum, as expected on a short period.)

**Outcome 1, as pre-registered:** 10 of 12 hold on 2026, 11 of 12 on 2016-17 (≥ 8 needed on each).

**What it shows, stepping back:**
- **2026 is the test that discriminates.** The coins fell (BTC −26%, ETH −39%, LTC −41%, XRP −47%; XMR +17%, ZEC
  +89%); holding the 6 coins had a Sharpe of about 0.1. The trend ideas, long-only and in the market 30 to 60% of the
  days, made 0.4 to 1.8: they stayed out of most of the falls and caught ZEC's and XMR's rises. 6 of 12 pass every
  step 6 bar on 2026.
- **2016-17 does not discriminate.** A bull market (BTC ×32): any idea that is long most of the time has a Sharpe
  near 3, and none beats holding. It shows the ideas are not broken in another market, not that they add value there.
- **The 10 are close to one result counted 10 times:** 9 are long-only "be in when the trend is up" ideas. "10 of 12"
  is one family holding, not 10 independent confirmations.
- **What fails:** the only reversal idea (night_005), on both periods; and rising-month weekly momentum, whose
  measure turns negative in 2026 (its book still earns, from the trend filter, not from its measure).

**Next, as pre-registered:** paper trading via the live session. Candidates: the ideas that hold on both periods and
pass step 6 on 2026 (6). Recommended first: momentum in uptrends (night_013) and high-RSI trend continuation
(validation; its uptrend twin is a near-duplicate): each confirmed on 2016-17 and profitable enough on 2026.

**Made standard** (2026-11-18): `orchestration/unseen_test/`, which `run_idea` calls for every confirmed and profitable
idea; it gives the same files as this run (its `validation/reading.md`).

**Spent:** the 2026 H1 holdout (recorded in the policy; the holdout is now 2027 H1). The next unseen dates are the
days after 2026-11-17 (`trading-bot/tools/extend_kraken_daily.py` adds them).
