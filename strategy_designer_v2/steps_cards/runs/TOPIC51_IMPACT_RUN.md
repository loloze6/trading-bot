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
(the session writes it here, with its table in `topics/51_review/impact.csv` and the script that made it)
