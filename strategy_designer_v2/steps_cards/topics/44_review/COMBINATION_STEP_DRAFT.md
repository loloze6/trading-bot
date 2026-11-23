# Draft: the combination function (topic 44; not built, for the operator)

Started 2026-11-23, the operator: "start thinking in parallel about the combination step logic that will be
implemented, keeping in mind it should not be a patch from our observations and that it should be standardized".
Shape: `HOW_WE_DESIGN_A_CARD.md`. Each rule is the general rule; its evidence is listed apart (below), so no rule is
written for one book or one run. To be revised with P4's reading (`runs/PORTFOLIO_UNSEEN_RUN.md`).

## Business objective, one question
**From every book the research has made, which portfolio earns the most for its risk, and does it hold on dates the
research never used?** A single real book rarely clears step 6's bar alone (topic 47: market timing on correlated
coins); unrelated books that each earn a little can together (topic 44, Seen). The function turns the register into
one portfolio, fixed, then tested like a book.

## Where it sits
An orchestration function beside `ideas_similarities_check` and `unseen_test`: it reads the register of books (every
run), not one idea. Called by hand for now (like the similarity check); later by `loop` when the register gains a book
that could enter. It decides nothing about ideas: step 7 and `select_next` never read it, so the search does not bend
towards what combines well (that would be a second search on the same dates).

## Input
- The register of books (`orchestration/ideas_similarities_check/register/books.json`) and each book's records:
  step 5's verdict and size, step 6's check, step 4's daily returns per window (`chart_bars.csv.gz`).
- The folds (`trading-bot/config/folds.yaml`) and the unseen periods (`common/unseen_dates.md`).

## Output
One portfolio version: `orchestration/combine/portfolios/<version>/` with `portfolio.json` (the books, their runs,
their weights rule, the date and the commit it was fixed at), the in-sample measures, then the unseen result; and one
line per version in `portfolios/INDEX.md`. A version is never changed after its unseen test is read: a new choice is a
new version, and every version tried stays listed (the count of versions is the visibility of any search on the
unseen dates).

## What a portfolio is (the business definition)
**Several books run side by side, each unchanged (its plan, config, coins, gate, holding period, costs), each with a
share of the capital; per coin, their positions added up.** A portfolio is judged as a book: the same measures (step 6)
on the folds, the same "holds" rule on the unseen dates. No measure or bar of its own.

## The rules (each general; evidence below)
| # | Rule | Evidence |
|---|---|---|
| R1 | **Admission:** a book enters the choice if its idea is real (step 5 confirmed), the idea's size at its horizon is above 0 (step 5's size), and the book earns on its own after costs in sample (step 6's Sharpe above 0). No bar on how strong: no threshold on Sharpe, size or t. | E1, E2, E3 |
| R2 | **One book per family** (the brief's idea it descends from), chosen without its results: the admitted book closest to the idea (fewest generations, then the earliest made). | E4 |
| R3 | **Unrelated:** families taken in a fixed order (brief number); a family's book enters if the correlation of its daily returns with every book already in is below 0.5 in size (the register's line: one explains under a quarter of the other). | E5, E6 |
| R4 | **Weights:** equal capital unless another standard rule wins out of fold. The function compares the same three rules each time (equal capital; equal risk from each book's past swing; equal risk contribution with the correlations), each recomputed from past days only and capped at 3 times the equal weight; a rule replaces equal capital only if it is chosen on at least 3 of the 4 folds (chosen on three, judged on the fourth) and beats equal capital on at least 3 held-out folds. | E7 |
| R5 | **Run in parallel** (the portfolio layer, option A): each book unchanged; per coin, the positions added up and one order for the difference. | E8 |
| R6 | **Fixed before it is seen:** the version (books, weights rule) is written and committed before its unseen test; its unseen result never changes it. | E9 |
| R7 | **Judged as a book:** step 6's measures and bars on the folds; on each unseen period, holds if its Sharpe after costs is above 0; next to it, its books alone and holding the coins. | E10 |

## Evidence (the observations the rules rest on)
| # | Observation | Where |
|---|---|---|
| E1 | Books that lose on their own sink any weighting: by P1's first rule (no earning condition), 7 of 25 candidates lose after costs, every weight rule loses (Calmar -0.21 to -0.16) while the median book earns (0.19). | `topics/44_review/p2_weights.csv`; topic 44 |
| E2 | The strongest in-sample results hold least on unseen dates (weakest third of step 5 strength holds 100 %, highest third 50 %). So no strength threshold. | topic 47, 1d-11 |
| E3 | A size above 0 says the idea exists, not that its book keeps it after costs (hourly gross already negative on many books; churn). | topic 47 1d-10; topic 48 obs. 6, 7, 9 |
| E4 | Variants of one idea are one bet: five books of one family combined, Calmar 0.70 against 0.80 for five families. | topic 47, 1d-7 |
| E5 | Correlation decides the gain: at 0.99 no reduction of the swing, at 0.90 about 3 %, at 0.64-0.71 no gain in Sharpe; at 0.05 Sharpe 1.26 and 1.23 alone, 1.66 together, the deepest fall halved. | `runs/COMBINE_TEST_RUN.md`; `runs/NIGHT4_RUN.md` test 2 |
| E6 | Unrelated stays unrelated out of sample (the momentum and reversal pair: +0.05 in sample, -0.15 and -0.11 on the unseen periods). | topic 44, Seen |
| E7 | Out of fold, equal capital chosen on 3 of 4 folds; the other choice did worse on its held-out fold. | `topics/44_review/p2_out_of_fold_earning.csv` |
| E8 | One config with weighted components changes the books (an idea off that day hands its weight to the other; one holding period): swing 60 % larger, deeper fall. | `runs/COMBINE_TEST_RUN.md`, method B |
| E9 | Choosing by results on the same dates inflates them (search luck: the n-th variant holds less; the reversal book paid on the folds and not out of sample). | topic 47 (study 2); topic 44, Seen |
| E10 | (to come) P4: the fixed portfolio on the unseen dates. | `runs/PORTFOLIO_UNSEEN_RUN.md` |

## Open (for the operator)
1. **The family's book (R2):** "closest to the idea" may keep a first, unfaithful book over a later repair that trades
   the idea as stated (topic 47 N3). Once books are built faithful (from 2026-11-23), the rule holds as is; for older
   books, an alternative is the latest generation. Not measured.
2. **The order of families (R3):** brief order decides which of two related families enters. It uses no result, but
   it is arbitrary; an alternative is to keep, of two related books, the one with more cases (more evidence). Not measured.
3. **Rebalancing:** P2 rebalances to the weights every day; a live layer would rebalance at a fixed interval (fewer
   orders). The interval's cost and effect are to be measured before the layer's card.
4. **Admission in sample (R1):** with hundreds of books, some earn above 0 by chance; the portfolio spreads that
   noise rather than removing it. Whether a book's unseen result should ever take it out is a question for the
   operator: today no (the unseen dates would become seen).
5. **Shorts:** short books need a venue that sells short (topic 09).

## What it does not do
It does not change a book, choose ideas, or read the unseen results to choose; it does not trade.
