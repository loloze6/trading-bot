# 1l's effect on our books (2026-11-25): steps 4 and 6 before and after topic 51's change (written before the run)

**The operator (2026-11-25):** "Same for 1l, should we observe more in detail the impacts of this change on previous
runs?" "Go for 2 in a dedicated session." Topic 51's proof showed the change does only what it should (7 books, 0
unexplained differences); this run measures what it changes in our results, before the merge into master.

## Purpose
One question: **which of our books change their step 6 answer, and how much do their measures and the portfolio's
move, when a move to flat is never refused by the band?**

## The books (42 and the candidates)
- P4's 20 (`topics/44_review/p1_candidates_earning.csv`, status candidate);
- night 7's new-code books confirmed by step 5 and profitable enough by step 6 (`topics/49_review/night7_ideas_full.csv`);
- P11's 2 (`topics/44_review/p7_night6_candidates.csv`, status candidate) and P13's (night 7's candidates).

## How
- **Before:** the engine of commit `e72a6b97f9` (before 1l: `trading-bot/core/trading_bot.py` and
  `trading-bot/risk/risk_manager.py` at that commit); **after:** the working branch. Both on the same plans and data,
  step 4 with `--out-root` to a scratch folder (nothing written over the committed records), then step 6
  (`06_profitability/helper/check_profitability.py`) on each record, to a scratch folder too.
- A record made with the same engine as `e72a6b97f9` (no commit to `trading-bot/core`, `risk` or `execution` between
  them) may stand as its own "before" from its committed chart file; say which.
- Step 5 should not change (its verdict reads the forecast and the prices, not the positions): checked on 5 books by
  rerunning their `measure.py` on both records.
- On both unseen periods (`04_backtest/windows/unseen_*.json`): P4's 20 and the candidates, before and after, and P4's
  portfolio (equal capital, as `topics/44_review/p4_portfolio.py`).

## Measured
Per book: step 6's answer before and after (flips named), Sharpe, Calmar, mean daily return on days in a position,
days in a position; for the specialists, the share of those days inside their profile. Per portfolio (P4's 20): Sharpe,
yearly return, worst fall, in-sample and on each unseen period. Allowed differences: those of topic 51's proof only.

## Expected
Days in a position fall (topic 51: 0 to 44 %); measures move little (Sharpe within about 0.1); a few books near step
6's thresholds may flip. A flip of a portfolio book, or a portfolio result moving by more than 0.1 Sharpe, is reported
for the operator before the merge.

## Reading
Session of 2026-11-25/26, 0 USD (no model call). Table: `topics/51_review/impact.csv` (one row per book and period;
98 book rows plus 3 P4 portfolio rows), made by `topics/51_review/impact.py`. 46 books: 39 daily, 7 hourly; 26 of them
also on the unseen periods (2016-17, 2026). Both engines run the current settings on the same plans and data.

**Which expected outcome happened.** Days in a position fell, and the measures moved little, as expected. No book
flipped at step 6. No portfolio result moved by more than 0.1 Sharpe. Nothing needs reporting before the merge.

**Step 6 flips: none** (0 of 98 book-periods). Five book-periods had one measure cross its threshold, but each answer
stayed "not profitable enough" because another measure still failed:

| Book | Period | Before | After | Measure that crossed | Sharpe before → after |
|---|---|---|---|---|---|
| 026-02 | in sample | not profitable enough | not profitable enough | mean daily return in a position | 0.217 → 0.216 |
| 017-05 | in sample | not profitable enough | not profitable enough | lowest Sharpe, one window left out | 0.207 → 0.190 |
| 026-01 | 2016-17 | not profitable enough | not profitable enough | lowest Sharpe one window out; Calmar | 1.004 → 0.613 |
| 029-05 | 2026 | not profitable enough | not profitable enough | Sharpe | 0.022 → −0.009 |
| 026-02 | 2026 | not profitable enough | not profitable enough | Sharpe | −0.087 → 0.072 |

All 26 "profitable enough" book-periods (24 in sample, 2 in 2026) keep that answer. Step 5 gives the same full verdict
before and after on all 5 books checked (038-01, 034-02, 035-01.b1, 002-03, 011-01.g1).

**Changes in Sharpe and in days in a position** (after minus before):

| Period | Books | Median Sharpe change | Median size of the change | Largest Sharpe change | Median change in days in a position | Largest fall in days | Days unchanged |
|---|---|---|---|---|---|---|---|
| In sample | 46 | 0.000 | 0.003 | 035-01.b1: 1.188 → 1.110 (−0.08) | −18 % | 026-04: 2,738 → 1,209 (−56 %) | 8 books |
| 2016-17 | 26 | 0.000 | 0.004 | 026-02: −2.121 → −1.642 (+0.48) | −7 % | 026-02: 660 → 212 (−68 %) | 10 books |
| 2026 | 26 | 0.000 | 0.003 | 026-02: −0.087 → 0.072 (+0.16) | −9 % | 003-02: 824 → 395 (−52 %) | 11 books |

Moves larger than 0.1 Sharpe are only on the unseen periods and only on books that were not profitable there:
026-02 (+0.48 in 2016-17, +0.16 in 2026), 026-01 (−0.39 in 2016-17), 026-04 (−0.15 in 2016-17), 029-03 (+0.12 in
2016-17). Their unseen periods hold few days in a position (hundreds), so a few exits more or less weigh a lot.

**Specialists: share of their days in a position inside their profile** (in sample, the 18 night 7 books that name a
profile). Before: 0.59 to 0.99. After: 0.74 to 1.00. All "falling agitated" and "agitated" books go to 0.99-1.00
(for example 035-01: 0.82 → 0.99 on 1,706 → 1,297 days). The "rising" books rise most but stay below 0.9: 034-01.b1
0.59 → 0.74, 034-02 0.64 → 0.83, 034-01.e1 0.65 → 0.85, 033-03.b2 0.74 → 0.89. 035-01.b1 ("calm"): 0.80 → 0.95.
045-01 (rising market, late-week gain) is unchanged at 0.99. So most of the days outside the profile were the
small positions the band refused to close.

**P4's portfolio** (equal capital, 20 books):

| Period | Sharpe before → after | Calmar before → after | Yearly return before → after | Worst fall before → after |
|---|---|---|---|---|
| In sample | 1.711 → 1.703 | 1.44 → 1.41 | 10.7 % → 10.7 % | 7.4 % → 7.5 % |
| 2016-17 | 1.079 → 1.074 | 0.61 → 0.62 | 6.7 % → 6.7 % | 11.1 % → 10.9 % |
| 2026 | −0.734 → −0.645 | −0.65 → −0.60 | −3.1 % → −2.8 % | 4.8 % → 4.6 % |

The largest move is 2026, +0.09 Sharpe, just under the 0.1 report line.

**Differences not explained by topic 51's named difference: none.** Topic 51's only change is that a move to flat is
never refused, so it can only end positions sooner. That matches what was measured: no book gained a day in a
position. No book changed Sharpe while keeping the same days in a position. 
Two things to know when reading the table:
- 7 committed P4 in-sample records (005-02, 006-04, 013-03, 011-01, 002-03, 003-02, 013-04) differ from the "before"
  rerun. They were made 2026-11-15 to 18 under older settings: other cost_model.slippage_bps (e.g. BTC 2.5 against 0.1
  now) and gap_rule ignore_max_bars 3 against 1. So they could not serve as "before". All "before" records are reruns
  on the current settings. The other 38 in-sample records and all 46 committed unseen records equal the rerun window by
  window. P4's "before" portfolio on the unseen periods matches the published figures (1.08 and −0.73).
- 032-02.b2's plan is not on this branch; it was taken from branch `night7c-panic` (no committed record to compare).
- Two books share the number 045-01 (agitated wide low close rebound; rising market late-week gain): the `id` column
  tells them apart.
