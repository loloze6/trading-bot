# Unseen coins run: does a book that is real and pays on its coins still hold on coins it was never tested on? (plan, 2026-11-25)

## Purpose
The operator (2026-11-25): the unseen dates (2016-17, 2026) are now used by the portfolio's choice (P4, P10b), paper
trading is too slow, and the sealed holdout is kept for one final verdict. The coins a plan never tested are data
nobody used for that plan. This run tests each book, unchanged, on its unseen coins over its own folds
(`common/unseen_coins.md`), with the rule the unseen dates use: holds when the main measure keeps its in-sample sign
AND the book's Sharpe after costs is above 0. It is the first use of the development judge for the combination method
(P6): a portfolio chosen by fixed rules in-sample, judged on unseen coins.

Cost: 0 USD of model calls (step 5 applies each idea's own `measure.py`); engine time only.

## The books (fixed before the run, from the committed files at 734cbff5b9)
44 books; the list is `runs/unseen_coins/books.tsv` (group, run, book).

| Group | Source | Books | With unseen coins |
|---|---|---|---|
| P4 | `topics/44_review/p1_candidates_earning.csv`, status candidate | 20 | 17 (021-02, 025-02, 025-03 tested all 19 coins) |
| P11 | `topics/44_review/p7_night6_candidates.csv`, status candidate | 2 | 1 (031-03.g1.b1 tested all 19) |
| N7 | `topics/49_review/night7_ideas_full.csv`, arm new, step 5 confirmed and step 6 profitable enough | 22 | 17 (the 5 rangefail books on 19 coins have none) |

Unseen coins per book: 13 for a book on the 6 default coins (ADA, AAVE, AVAX, DOGE, INJ, LINK, NEAR, ONDO, SOL, SUI,
TAO, TRX, UNI); 17 for 005-02 (BTC, ETH, BNB) and 028-04 (BTC, ETH); 4 for 002-03 (NEAR, ONDO, SUI, TAO: fold D only).
Of the 35 books with unseen coins, 28 are daily and 7 hourly (017-01, 017-05, 026-01 to 026-04, 028-04).

## How it is run
- Per book: `python3 orchestration/unseen_test/helper/unseen_test.py PLAN --run RUN --python VENV --coins`
  (step 4 with `--coins`, step 5 with `--measure`, step 6). Records under each book's own run, in `unseen_coins/`,
  beside its unseen periods; its result is the entry `unseen_coins` of `orchestration/unseen_test/<run>/<id>.json`,
  and its index line.
- One background job over the list, in order; a book whose files exist is not run again (resume).
- The P4 portfolio on unseen coins: `topics/44_review/p4_portfolio.py unseen_coins` (the P4 method unchanged: equal
  capital among the books with a record, each book's daily returns by step 6's definition).

## Expected outcomes (written before the run)
1. **Most books hold on their unseen coins: 70 % or more of the 35.** Coins move together and the years are the same,
   so an idea that rode its folds' market should still earn on other coins; this run tests the coins, not the years.
2. **More books hold on unseen coins than on 2026** (P4: 4 of 20 held on 2026, 6 of 20 on 2016-17; night 7: 9 of 22
   on 2026, 18 of 22 on 2016-17). If fewer hold, the in-sample results depend on the 6 default coins (XMR's and ZEC's own histories).
3. **P4's portfolio holds on unseen coins** (Sharpe above 0), below its in-sample Sharpe (1.64).
4. **Books that failed both unseen periods fail unseen coins more often than those that held on both.**
5. **Failures to expect, not counted as "does not hold":** the 9 books on all 19 coins ("none"); a coin listed late
   runs few windows; an idea's `measure.py` may refuse a record on other coins (then "no verdict" and "does not hold",
   named in the reading).

What would change a decision: a book that does not hold on unseen coins is fitted to its coins; the combination method
(P6) would then use unseen coins as its development judge before the sealed holdout.

## Reading (after the run)
To be written.
