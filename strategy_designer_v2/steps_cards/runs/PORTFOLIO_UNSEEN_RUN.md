# Portfolio unseen run: does a fixed portfolio of real books hold on dates the research never used? (plan, 2026-11-23)

## Purpose
Topic 44, P4. The candidates and the weights were chosen on the folds only (P1, P2: `topics/44_review/`). This run
fixes one portfolio now, before any of its unseen results is read, and judges it on the unseen dates
(`common/unseen_dates.md`), against its books alone.

## The portfolio, fixed (2026-11-23, before any unseen result of these books is read)
- **Books:** the 20 candidates of `topics/44_review/p1_candidates_earning.csv` (commit edef99840b): one per family,
  real by step 5, size above 0, step 6's Sharpe above 0 in sample, daily returns correlated under 0.5 with every book
  already in (families in brief order). The operator's go: 2026-11-23 ("Go").
- **Weights:** equal capital (P2: chosen out of fold on 3 of 4 folds). Run in parallel, each book with its own plan,
  config, coins and costs, unchanged (P3).
- **Known before:** book 18 (028-04, the one paying book) had an unseen test in `night4_volumehour_run` before this
  run; its result did not enter P1 or P2. No other book of the 20 had one.

| # | Family | Bar | Run | Book | Step 5 / 6 | In-sample Sharpe |
|---|---|---|---|---|---|---|
| 1 | 002-03 | 1d | validation_run | b1_distance-above-200-day-more-coins_1d | confirmed / not paying | 0.84 |
| 2 | 003-02 | 1d | volume_run | g1_heavy-volume-up-moves-continue_1d | confirmed / not paying | 0.10 |
| 3 | 005-02 | 1d | night_005_run | g1_volatile-day-move-reversal_1d | confirmed / not paying | 0.43 |
| 4 | 006-04 | 1d | night_006_run | g1_volume-surge-precedes-rise_1d | confirmed / not paying | 0.78 |
| 5 | 011-01 | 1d | night_run | g1_volatile-day-selloffs-bounce-next_1d | confirmed / not paying | 0.73 |
| 6 | 013-03 | 1d | night_013_run | g1_near-30-day-high-continuation_1d | confirmed / not paying | 0.29 |
| 7 | 013-04 | 1d | volume_run | heavy-volume-below-high-breakout_1d | confirmed / not paying | 0.51 |
| 8 | 017-01 | 1h | retest_settlement_run | d1_hourly-shock-reverses-over-day_1h | confirmed / not paying | 0.19 |
| 9 | 017-05 | 1h | step7ab_b_run | d3_midnight-settlement-daily-reversal_1h | confirmed / not paying | 0.21 |
| 10 | 021-02 | 1d | night3_ichimoku_run | b1_slow-cloud-fall-more-coins_1d | confirmed / not paying | 0.17 |
| 11 | 022-04 | 1d | night3_learned_run | b2_volatility-power-turns-around_1d | confirmed / not paying | 0.68 |
| 12 | 025-02 | 1d | night4_fallingbounce_run | b1_bounce-fades-in-monthly-fall_1d | confirmed / not paying | 0.59 |
| 13 | 025-03 | 1d | night4_fallingbounce_run | b1_falling-regime-bounce-all-coins_1d | confirmed / not paying | 0.81 |
| 14 | 026-01 | 1h | night4_weekend_run | d1_calm-regime-weekend-move-continues_1h | confirmed / not paying | 0.50 |
| 15 | 026-02 | 1h | night4_weekend_run | d2_weekend-break-of-rising-week_1h | confirmed / not paying | 0.22 |
| 16 | 026-03 | 1h | night4_weekend_run | b1_midweek-moves-continue-into-weekend_1h | confirmed / not paying | 0.26 |
| 17 | 026-04 | 1h | retest_weekend_run | b2_heavy-weekend-moves-continue_1h | confirmed / not paying | 0.90 |
| 18 | 028-04 | 1h | night4_volumehour_run | b1_quiet-dip-in-uptrend-recovers_1h | confirmed / paying | 0.98 |
| 19 | 029-03 | 1d | short_1d_run | d1_failed-breakout-after-small-run-up_1d | confirmed / not paying | 0.53 |
| 20 | 029-05 | 1d | short_1d_run | b1_volatility-scaled-failed-breakout-depth_1d | confirmed / not paying | 0.39 |

## How it is run
- Each book: `orchestration/unseen_test/helper/unseen_test.py PLAN --run RUN` (steps 4, 5, 6 on each unseen period,
  its measure unchanged, no model call), its files in its own run's folders.
- Data: the daily books read the daily files (to 2026-11-17). The 7 hourly books trade BTC, ETH, LTC, XMR, XRP, ZEC:
  their hourly files end on 2025-12-31, so they are extended first to 2026-11-17 by `trading-bot/tools/extend_kraken_hourly.py`
  (Kraken's 2026 Q1-Q3 archive, then Kraken's public trades; the trades are used only if they rebuild the archive's
  last day exactly). 2016-2017 hourly bars are already in the files.
- The portfolio, per period (`topics/44_review/p4_portfolio.py`): its daily return is the mean of the daily returns
  of the books that have a record on that period (equal capital among them; a book with no record there is named and
  left out of that period).

## How it is read (fixed now)
- **The portfolio holds on a period** when its Sharpe after costs is above 0 there (the book part of the "holds" rule
  of `common/unseen_dates.md`). Next to it: its Calmar, yearly return, worst fall; holding the coins (equal weight of
  the coins the books trade) on the same days.
- **Against its books alone:** how many books hold (each book's own unseen rule), and their median Sharpe.

## Expected outcomes, written before
| Outcome | What it would mean | Next |
|---|---|---|
| A. Holds on both periods, and its Sharpe above its books' median | combining real books is worth building | P5: the portfolio layer's card, the operator's go |
| B. Holds on one period only | the in-sample gain is partly the folds' own; one period is short (2026: 11 months) | read which books carry it; no build yet |
| C. Holds on neither | the in-sample result (Calmar 1.37) was selection: these books do not hold together | back to topic 47: why real books do not hold |
The designer's guess, for the record: B, holding on 2016-2017 (a rising market; most daily books lean long) and not
on 2026 (a falling market for most coins).

## Reading (2026-11-24, about 10:35 Paris)
All 20 books run on both unseen periods (the 7 hourly books after their 2026 bars were fetched: 6 coins, Kraken's 2026
archive then its public trades, each checked against the archive; `trading-bot/tools/extend_kraken_hourly.py`).
`topics/44_review/p4_portfolio.py`, `p4_portfolio.csv`, `p4_books.csv`.

| | 2016-17 (rising market) | 2026 (falling market) |
|---|---|---|
| **Portfolio: Sharpe** | **1.08: holds** | **-0.73: does not hold** |
| Portfolio: Calmar, yearly, worst fall | 0.61, +6.7 %, 11.1 % | -0.66, -3.1 %, 4.8 % |
| Holding the coins: Sharpe, yearly, worst fall | 3.63, x12, 41.1 % | 0.02, -14.2 %, 44.5 % |
| The books alone: holding / Sharpe above 0 / median Sharpe | 6 / 10 of 20 / 0.30 | 4 / 8 of 20 / -0.08 |
| Correlation between books (mean) / with holding | 0.01 / 0.50 | 0.00 / 0.06 |

**Outcome B** (the designer's guess): holds on one period only. The portfolio does what combining promises on risk (its
worst fall 11 % and 5 % against 41 % and 45 % for holding; its books nearly uncorrelated on both periods), but not on
return: on 2026 its books lose on average (median Sharpe -0.08), and an average of losing books loses less, not
nothing.

**Where it comes from:**
- The daily books lean long (002-03, 003-02, 006-04, 011-01, 025-03: long 34 to 81 % of coin-days); they carry 2016-17
  and lose on 2026. The two books with no net lean, 013-03 and 013-04 (a coin near its recent high, heavy volume below
  its yearly high), earn on both periods (Sharpe 1.84 and 1.70; 1.94 and 0.87).
- The 7 hourly books add little: on 2016-17 they take the portfolio's Sharpe from 2.34 (the 14 books read first) to 1.08;
  1 of the 7 holds on one period (026-03, 2026 only). Their in-sample Sharpe was 0.19 to 0.98.
- The in-sample result (Calmar 1.37) was selection: the books were kept for earning on those same dates.

**Next (for the operator):** no portfolio layer build (P5 waits). Two questions this answers in part: P8 (a rule on
market exposure: the books with no net lean held, the leaning ones followed the market) and the candidates (P1's rule
admits books with an in-sample Sharpe as low as 0.10; the books that held had no lower in-sample strength than those
that did not, topic 47 1d-11). Note: these unseen periods are now seen for this portfolio; a new rule is judged on new
dates.
