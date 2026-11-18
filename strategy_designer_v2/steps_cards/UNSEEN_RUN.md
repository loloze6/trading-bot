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
