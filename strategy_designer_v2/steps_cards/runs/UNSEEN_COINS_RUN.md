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

- **The engine:** this branch's, from 734cbff5b9, which holds 1l (topic 51: a move to flat is never refused by the
  band; not yet on master). The in-sample verdicts and the unseen-dates results were made before 1l. Step 5's main
  measure does not change with 1l (it reads forecasts and prices); step 6's Sharpe moves by up to 0.08 on topic 51's 7
  proof books (`topics/51_review/compare.csv`). So the holds rule's in-sample sign is unaffected; the comparison with
  the unseen dates carries that small difference. Proof that step 4 without `--coins` is unchanged: the helper of
  734cbff5b9 and this branch's, on 048-01 and unseen_2026, give identical files (metrics, bars, trades, chart files,
  run.md) apart from the manifests, logs and run summaries (times and run ids).

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

## Reading (after the run, 2026-11-25)
All 44 books ran (exit 0), 0 USD of model calls. Table: `runs/unseen_coins/table.csv` (from `runs/unseen_coins/reading.py`).

**In short:** 27 of the 35 books with unseen coins hold (77 %), more than on either unseen period. But on these coins
over these years, simply holding them earned a Sharpe of about 1.0, so "Sharpe above 0" is a low bar: only 9 of the
35 beat holding. Daily books carry to other coins (25 of 28 hold); hourly books mostly do not (2 of 7).

| | Books with unseen coins | Hold | Beat holding's Sharpe | None (tested all 19 coins) |
|---|---|---|---|---|
| P4 | 17 | 9 | 1 | 3 |
| P11 | 1 | 1 | 0 | 1 |
| N7 | 17 | 17 | 8 | 5 |
| All | 35 | 27 | 9 | 9 |

**P4's 20:** 9 hold, 8 do not, 3 have no unseen coins (021-02, 025-02, 025-03).
**P4's portfolio (equal capital, the 17 with a record, `topics/44_review/p4_portfolio_unseen_coins.csv`):** Sharpe
0.26 (holds), against 1.51 in-sample for the same 17 books, and against 0.68 for holding the same coins. It makes
1.3 % a year with a worst fall of 17 %; holding made 21.5 % a year with a worst fall of 89 %. Its correlation with holding is 0.32.

**Against the unseen dates (books with unseen coins):**

| 2016-17 | 2026 | Books | Hold on unseen coins |
|---|---|---|---|
| holds | holds | 5 | 5 |
| holds | does not hold | 15 | 15 |
| does not hold | holds | 4 | 2 |
| does not hold | does not hold | 11 | 5 |

**Expected outcomes, which happened:**
1. 70 % or more hold: **yes** (77 %), carried by night 7 (17 of 17). P4 alone: 53 % (9 of 17).
2. More hold than on 2026: **yes** (P4 9 of 17 against 4 of 20; N7 17 of 17 against 9 of 22).
3. P4's portfolio holds, below in-sample: **yes** (0.26 against 1.51). It is also below holding (0.68).
4. Books that failed both unseen periods fail more often: **yes** (5 of 11 hold, against 5 of 5 that held both).
5. The failures expected: the 9 "none" books, as expected. No `measure.py` refused a record (0 "no verdict" among the 35).
   Step 5's verdict on unseen coins: 12 confirmed, 21 inconclusive, 2 not observable. The holds rule reads only the sign.

**What it shows (a practitioner's reading):**
- **The hourly books do not carry.** 017-01, 017-05, 026-01, 026-02 and 028-04 have negative Sharpe. This is not a cost
  problem: 017-01, 017-05 and 026-01 lose money before costs on these coins (026-02 makes +360 before costs, then loses
  it to costs). Their in-sample edge looks fitted to their coins.
- **The night 7 books are not 17 independent results.** They are mostly "agitated fall, then rebound" ideas. Three
  books have exactly the same unseen-coins Sharpe (035-01, 038-02, 051-01: 0.7995). Two more pairs match each other
  (047-01 and 038-01: 0.862). So 17 of 17 counts the same edge several times.
- **The bar is low on these coins.** The other coins rose a great deal over these years (holding's Sharpe is about 1.0
  for almost every book). A book that is mostly long earns there. Unseen coins catch a fit to a few coins (the hourly
  books, 022-04, 029-03, 029-05). They do not catch a fit to the years: that is what the unseen dates catch, as
  `common/unseen_coins.md` says.
- **One change a practitioner would make next:** compare each book with holding on the same coins, not only with 0.
  This would be a rule change (to `unseen_dates.md`'s holds), so it is the operator's decision, not made here.
  Today 9 of 35 pass that test.

**Failures, skips and caveats:**
- Step 4 skipped 4520 coin-windows for lack of data (a coin not yet listed), and the engine refused 1287 for warm-up
  (the windows right after a coin's listing: "the engine stopped"). These count as not run, not as losses. This is why
  a book on 13 coins runs 124 to 162 coin-windows out of 13 × 24.
- 022-04 ran 11 of its 13 coins (2 had no window that ran).
- **Corrected from the plan above:** 002-03's 4 coins are not "fold D only". It ran 18 coin-windows over 2.65 years,
  because NEAR (and part of the others) has data in fold A. `common/data_available.md` (line 15) also says "fold D
  only: NEAR, SUI, TAO, ONDO". That line needs a correction; it is noted here, not changed.
- The batch over books 4-20 was cut at the 2-hour background limit while 026-03 was in step 4. Its partial record was
  deleted, and the book was rerun in full. Nothing else was cut.
- Engine: this branch's, with 1l (see above). The unseen-dates and in-sample results were made before 1l.
- No `trading-bot/` or `strategy-research/` code was changed. Step 4's `--coins` is in `steps_cards/04_backtest/`.

**Per book** (main measure: unseen coins, then in-sample in brackets; Sharpe: book, then holding in brackets):

| Group | Book | Bar | Unseen coins | Coins ran | Years | Main (in-sample) | Sharpe (holding) | In-sample Sharpe | 2016-17 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| P4 | 002-03 | 1d | **holds** | 4 of 4 | 2.65 | 0.01352 (0.00404) | 0.9511 (0.7649) | 0.8416 | holds | does not hold |
| P4 | 003-02 | 1d | **holds** | 13 of 13 | 6.95 | 0.01905 (0.01688) | 0.6423 (0.9937) | 0.1019 | holds | does not hold |
| P4 | 005-02 | 1d | **holds** | 17 of 17 | 7.94 | 0.0004216 (0.000786) | 0.5358 (0.5455) | 0.4326 | does not hold | does not hold |
| P4 | 006-04 | 1d | **holds** | 13 of 13 | 6.95 | 0.0004149 (0.0005309) | 0.9086 (0.9937) | 0.7845 | holds | does not hold |
| P4 | 011-01 | 1d | **holds** | 13 of 13 | 6.95 | 0.002937 (0.006223) | 0.5198 (0.9743) | 0.7317 | holds | does not hold |
| P4 | 013-03 | 1d | **holds** | 13 of 13 | 6.95 | 0.00303 (0.003478) | 0.9872 (0.9937) | 0.2851 | holds | holds |
| P4 | 013-04 | 1d | **holds** | 13 of 13 | 5.96 | 0.02782 (0.0358) | 0.3891 (1.146) | 0.5053 | does not hold | does not hold |
| P4 | 017-01 | 1h | **does not hold** | 13 of 13 | 6.95 | 3.024 (4.827) | -0.696 (0.9937) | 0.1873 | does not hold | does not hold |
| P4 | 017-05 | 1h | **does not hold** | 13 of 13 | 6.95 | -1.37e-05 (0.0001518) | -0.4167 (0.9937) | 0.2069 | does not hold | does not hold |
| P4 | 021-02 | 1d | none | 0 | - | - | - | 0.1719 | does not hold | does not hold |
| P4 | 022-04 | 1d | **does not hold** | 11 of 13 | 5.63 | 0.0008068 (0.002944) | -0.005303 (0.9922) | 0.6773 | does not hold | holds |
| P4 | 025-02 | 1d | none | 0 | - | - | - | 0.5945 | does not hold | does not hold |
| P4 | 025-03 | 1d | none | 0 | - | - | - | 0.8109 | holds | does not hold |
| P4 | 026-01 | 1h | **does not hold** | 13 of 13 | 6.29 | -0.0003217 (0.006944) | -0.1739 (0.9825) | 0.4961 | does not hold | does not hold |
| P4 | 026-02 | 1h | **does not hold** | 13 of 13 | 6.95 | 0.008809 (0.007628) | -0.06283 (0.9937) | 0.2166 | does not hold | does not hold |
| P4 | 026-03 | 1h | **holds** | 13 of 13 | 6.95 | 0.0005643 (0.0003197) | 0.287 (0.9937) | 0.2605 | does not hold | holds |
| P4 | 026-04 | 1h | **holds** | 13 of 13 | 6.95 | 0.001487 (0.01098) | 0.4282 (0.9937) | 0.8957 | does not hold | does not hold |
| P4 | 028-04 | 1h | **does not hold** | 17 of 17 | 7.94 | 0.001075 (0.001264) | -0.2117 (0.5721) | 0.9822 | does not hold | does not hold |
| P4 | 029-03 | 1d | **does not hold** | 13 of 13 | 6.95 | 0.006425 (0.02832) | -0.1256 (0.9937) | 0.5265 | does not hold | does not hold |
| P4 | 029-05 | 1d | **does not hold** | 13 of 13 | 6.62 | 0.0111 (0.02003) | -0.4566 (0.9484) | 0.3871 | does not hold | holds |
| P11 | 031-03.g1.b1 | 1d | none | 0 | - | - | - | 0.5663 | - | - |
| P11 | 031-01.g1 | 1d | **holds** | 13 of 13 | 6.95 | 0.01006 (0.008925) | 0.9332 (0.9937) | 1.007 | holds | does not hold |
| N7 | 033-03.b2 | 1d | **holds** | 13 of 13 | 6.95 | 0.1986 (3.085) | 0.975 (0.9937) | 0.919 | holds | holds |
| N7 | 034-02 | 1d | none | 0 | - | - | - | 1.351 | holds | holds |
| N7 | 035-02 | 1d | none | 0 | - | - | - | 1.228 | holds | holds |
| N7 | 034-01.e1 | 1d | none | 0 | - | - | - | 1.298 | holds | holds |
| N7 | 034-01.b1 | 1d | none | 0 | - | - | - | 1.249 | holds | holds |
| N7 | 035-01.b1 | 1d | none | 0 | - | - | - | 1.188 | does not hold | does not hold |
| N7 | 035-01 | 1d | **holds** | 13 of 13 | 5.96 | 0.0004776 (0.001055) | 0.7995 (1.004) | 1.049 | holds | does not hold |
| N7 | 043-01 | 1d | **holds** | 13 of 13 | 5.96 | 0.0005491 (0.0009248) | 0.902 (1.004) | 1.104 | holds | does not hold |
| N7 | 039-02.d1 | 1d | **holds** | 13 of 13 | 5.96 | 0.0009489 (0.001089) | 1.209 (1.004) | 0.976 | holds | does not hold |
| N7 | 044-01 | 1d | **holds** | 13 of 13 | 5.96 | 0.000703 (0.0004401) | 1.25 (1.004) | 0.9244 | holds | holds |
| N7 | 044-02 | 1d | **holds** | 13 of 13 | 5.96 | 0.00417 (0.005755) | 1.205 (1.004) | 1.111 | holds | holds |
| N7 | 045-01 | 1d | **holds** | 13 of 13 | 5.96 | 0.0005197 (0.0006699) | 1.165 (1.004) | 0.9146 | does not hold | does not hold |
| N7 | 047-01 | 1d | **holds** | 13 of 13 | 5.96 | 0.0004528 (0.001071) | 0.862 (1.004) | 1.072 | holds | does not hold |
| N7 | 038-01 | 1d | **holds** | 13 of 13 | 5.96 | 0.0004528 (0.001071) | 0.862 (1.004) | 1.072 | holds | does not hold |
| N7 | 038-02 | 1d | **holds** | 13 of 13 | 5.96 | 0.0004776 (0.001055) | 0.7995 (1.004) | 1.049 | holds | does not hold |
| N7 | 039-02 | 1d | **holds** | 13 of 13 | 5.96 | 0.003372 (0.005434) | 1.115 (1.004) | 0.9254 | holds | does not hold |
| N7 | 034-01.d1 | 1d | **holds** | 13 of 13 | 5.96 | 0.0005168 (0.0006241) | 1.139 (1.004) | 0.8737 | does not hold | does not hold |
| N7 | 041-03 | 1d | **holds** | 13 of 13 | 5.96 | 0.003635 (0.0107) | 0.8133 (1.004) | 1.124 | holds | does not hold |
| N7 | 045-01 | 1d | **holds** | 13 of 13 | 6.95 | 0.02011 (0.01295) | 1.503 (0.9743) | 1.088 | does not hold | holds |
| N7 | 048-01 | 1d | **holds** | 13 of 13 | 6.95 | 0.0008182 (0.000951) | 1.32 (0.9937) | 1.115 | holds | holds |
| N7 | 051-01 | 1d | **holds** | 13 of 13 | 5.96 | 0.002309 (0.007035) | 0.7995 (1.004) | 1.049 | holds | does not hold |
| N7 | 041-02 | 1d | **holds** | 13 of 13 | 6.95 | 5.545 (5.826) | 0.8574 (0.9937) | 0.7715 | holds | does not hold |
