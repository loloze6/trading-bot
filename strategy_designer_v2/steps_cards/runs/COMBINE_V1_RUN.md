# combine v1 on the unseen coins (2026-11-25; written before the run)

**The operator (2026-11-25):** "Go, let's try and iterate if necessary"; "you can try it in a new session". The
combination card (`orchestration/combine/card.md`) built its first version in-sample (`orchestration/combine/portfolios/v1/`:
9 of 109 books, Sharpe 1.97; the same 9 at equal weight 1.95; P4's 20, 1.48). In-sample proves nothing: this run
judges it on the development judge, the unseen coins (next steps 1u, `common/unseen_coins.md` on branch `unseen-coins`).

## Purpose
One question: **does v1, built by fixed rules, hold on coins none of its strategies was tested on, and does it do
better there than the two portfolios fixed beforehand?**

## The portfolios (fixed now, unchanged by this run)
| Portfolio | What |
|---|---|
| v1 | the 9 books of `portfolios/v1/portfolio.json`, their weights |
| (a) | the same 9 books at equal weight |
| P4 | P4's 20 strategies at equal weight |
All three by the card's rule 6 (coin by coin, the weighted sum of the books' returns, then the mean over coins), on each
book's unseen coins over its own folds.

## Expected outcomes (one of them)
| # | Outcome | Shown by |
|---|---|---|
| O1 | v1 holds and does better than (a) and P4 | Sharpe after costs above 0; v1's above both |
| O2 | v1 holds, no better than (a) | the box weighting adds nothing over equal weight |
| O3 | v1 does not hold | Sharpe at or below 0 |
Also reported: each book alone on its unseen coins (holds or not), how many coins and days each portfolio rests on, and
what was skipped.

## Reading (2026-11-25, after the run)
**Outcome: O1 by the rule written before the run (v1's Sharpe 0.99, above (a)'s 0.99 and P4's 0.13), but v1 is above
(a) by 0.003 only: in substance the box weighting adds nothing over equal weight (O2's reading).** Both hold on the
unseen coins; P4's 20 at equal weight barely earns there.

How it was computed: `orchestration/combine/helper/judge_unseen.py --version v1` (new), which calls `combine.py`'s own
portfolio function (rule 6) with a new `records` option reading `04_backtest/<run>/unseen_coins/backtests/<id>/` in place of
the in-sample record. No portfolio, weight or book changed. Proof that `combine.py` is unchanged in-sample: before and
after, on v1's 6 books whose in-sample records are on this machine, identical daily series.

| Portfolio | Books with an unseen-coins record | Coins | Days (years) | Sharpe | Yearly return | Worst fall | Calmar | In-sample Sharpe |
|---|---|---|---|---|---|---|---|---|
| v1 (its weights) | 8 of 9 | 17 | 2,897 (2018-2025) | **0.99** | 8.4 % | 8.9 % | 0.94 | 1.97 |
| (a) same 9, equal weight | 8 of 9 | 17 | 2,897 (2018-2025) | **0.99** (0.986) | 6.5 % | 6.9 % | 0.93 | 1.95 |
| P4's 20, equal weight | 17 of 20 | 17 | 2,897 (2018-2025) | **0.13** | 0.4 % | 9.3 % | 0.04 | 1.48 |
Coin by coin, then the mean over the coins of each day; a day where no book has a coin counts as 0. v1 earns more than (a)
because its weights add to more than 1 (1.33): more money in the same bets, with a deeper fall in proportion (Calmar
the same). Overlap (positions adding to more than one full position): 0.1 % of coin-days for v1.

**Each v1 book alone on its unseen coins** (holds: main measure with its in-sample sign AND Sharpe after costs above 0)
| Book | Coins | Coin-windows | Years | Main in-sample → unseen | Sharpe (holding's) | Step 6 | Holds |
|---|---|---|---|---|---|---|---|
| 026-03…d1 saturday continuation (1h) | 13 | 122 | 6.0 | 0.00125 → 0.00033 | 0.60 (1.04) | not enough | yes |
| 035-01 falling-agitated rebound | 13 | 124 | 6.0 | 0.00106 → 0.00048 | 0.80 (1.00) | not enough | yes |
| 001-01…c1 high-RSI continuation | 13 | 162 | 7.0 | 0.00198 → 0.00273 | 1.49 (0.99) | profitable enough | yes |
| 005-02…g2 volatile reversal | 17 | 252 | 7.9 | 0.0201 → 0.0141 | 0.35 (0.55) | not enough | yes |
| 010-03…e1 RSI side next week | 17 | 258 | 7.9 | 0.0134 → 0.0148 | 0.61 (0.57) | not enough | yes |
| 028-04.b1 quiet dip in uptrend (1h) | 17 | 258 | 7.9 | 0.00126 → 0.00107 | -0.21 (0.57) | not enough | **no** |
| 030-03…d1 heavy-volume bottom close | 13 | 162 | 7.0 | 0.00128 → 0.00045 | 0.98 (0.99) | not enough | yes |
| 011-01…d1 weekend reversal | – | – | – | – | – | – | none: tested all 19 coins |
| 031-01.g1 weekly gains into saturday | 13 | 162 | 7.0 | 0.00892 → 0.01006 | 0.93 (0.99) | not enough | yes |
**7 of 8 hold.** But only 2 of 8 beat holding the same coins (001-01…c1, 010-03…e1), and only 001-01…c1 is "profitable enough" by step 6;
the main measures keep their sign, mostly smaller (5 of 8). P4's books alone: 9 hold, 8 do not, 3 none.

**What it can and cannot show** (`common/unseen_coins.md`): it tests the coins, not the dates. The years are the folds'
(2018-2025 on these coins), the market the strategies were built in; coins move together, so a long-biased
book earns on any coin of a rising market. The sealed holdout and the unseen dates remain the judges of the years.
Relatives: 011-01…d1's family ran "on more coins" (it tested all 19), so it adds nothing here.

**Skipped or untested**
- 011-01…d1 (v1, weight 0.14) and 3 of P4's 20 (021-02, 025-02, 025-03) have no unseen coin: they add nothing to the portfolios.
- Backtest windows not run, per v1 book: 130 to 143 for no data on the venue (the coins are younger), and 13 (58 for
  026-03…d1 and 035-01) "the engine stopped", which the unseen-coins table counts as warm-up refusals (not checked here).
- v1's in-sample 1.97 cannot be rebuilt on this machine: the 3 `paying_rerun_run` books have no in-sample bars here (no
  chart file committed); on the other 6, the in-sample series is unchanged by this run's edit.
- P4 here is rule 6 on the coin-day records, not `topics/44_review/p4_portfolio.py` (step 6's daily returns, equal
  capital); the other session's P4 figure may differ.

Records: this session ran 6 v1 books (026-03…d1, 001-01…c1, 005-02…g2, 010-03…e1, 030-03…d1, 011-01…d1); the other
session (`unseen-coins`) the rest. Measures: `orchestration/combine/portfolios/v1/measures.json` (`unseen_coins`).
