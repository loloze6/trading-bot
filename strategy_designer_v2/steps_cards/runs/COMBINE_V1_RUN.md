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

## Reading
(the session writes it here)
