# Topic 55: data use and stage moves: which data each research step reads, and how a result moves to the next stage

Status: running (a draft for the operator's review; next steps A4)
Where: research: every step, the unseen tests, the combination, the sealed holdout; becomes a shared definition
(`common/`) once agreed
Opened: 2026-11-26, the operator: "have a full process agreed between fold and currency used, from ideas,
confirmation, combination, test ... standardize this so that we close this topic and it is processed following
guideline, not my decision"; then: "A4 is more global around data usage in the various research steps and automated
unlock of the next step".

(Shared definition, `../HOW_WE_DESIGN_A_CARD.md`. Next steps A4: the operator, 2026-11-26: "have a full process agreed
between fold and currency used, from ideas, confirmation, combination, test ... standardize this so that we close this
topic and it is processed following guideline, not my decision". It gathers rules already defined in their own cards
(they stay the reference: `explore_and_check.md`, `unseen_dates.md`, `unseen_coins.md`, `orchestration/combine/card.md`,
`trading-bot/config/campaign_data_policy.yaml`) and adds the two that were missing: the holds rule against holding
(C1) and the opening of the sealed holdout.)

## Business objective, one question
**At each stage of the research, which data may it read, so that every verdict is made on data that did not choose
what it judges, and the final verdict is made once on data nobody used?**
Why: a result judged on the data that chose it proves nothing; each judge loses its value once a choice reads it (the
unseen dates were used by P4 and P10b's choices; the unseen coins are now the development judge).

## The data (named by fold and years, never by window dates)
| Name | What | Coins |
|---|---|---|
| The exploration folds | folds B and C (2018 to 2021) | the plan's coins |
| The check folds | folds A and D (2022 to 2025) | the plan's coins |
| The folds | A to D together (2018 to 2025): the in-sample data | the plan's coins (the 6 default coins unless the plan names more) |
| The unseen dates | 2016-17 and 2026: two periods outside the folds | the plan's coins |
| The unseen coins | the folds, on the coins a plan did not test (`data_available.md`) | the other 13 coins |
| The sealed holdout | its dates only in `trading-bot/config/campaign_data_policy.yaml`; its data never opened by a step | — |

## The stages
| Stage | Reads | Never reads | Its rule (where it is defined) |
|---|---|---|---|
| Step 1, the brief; step 2, the ideas | no data (closed-book) | any data | `01_brief/card.md`, `02_ideation/card.md` |
| Step 7, the analysts (new ideas from a backtest) | the exploration folds | the check folds, the unseen dates and coins, the holdout | `explore_and_check.md` |
| Steps 3 and 4, the plan and its backtest | the folds | the rest | the plan's coins and folds |
| Step 5, is the idea real | the folds; a confirm's direction checked on the check folds alone | the rest | `explore_and_check.md` |
| Step 6, does its book pay | the folds | the rest | `06_profitability/helper/rule.yaml` |
| The unseen dates test (every confirmed and profitable book, unchanged) | the unseen dates | — | holds: `unseen_dates.md` (and rule H below) |
| The unseen coins test (the same books, unchanged) | the unseen coins | — | holds: `unseen_coins.md` (and rule H below) |
| `select_next`, the loop, step 7's lines | the folds' results | the unseen dates' and coins' results (no choice reads them) | `unseen_dates.md` |
| The combination: choosing a version | the folds' results only | the unseen dates' and coins' results | `orchestration/combine/card.md`, rules 1 to 5 |
| The combination: judging a version | the unseen coins (the development judge), then shown on the unseen dates | — | rule 6; every version listed (`portfolios/INDEX.md`) |
| The sealed holdout | once, for one version, by rule O below | — | rule O |

## The two rules added
- **H. Holds (next steps C1; the operator, 2026-11-26: portfolio only):** a book alone holds on unseen data when its
  main measure keeps its in-sample sign AND its Sharpe after costs is above 0 (today's rule, unchanged). A portfolio
  holds when, in addition, its Sharpe is above holding the same coins over the same days. Why: on the unseen coins
  holding earned a Sharpe of about 1.0 (27 of 35 books passed "above 0", 9 "above holding",
  `runs/UNSEEN_COINS_RUN.md`); a short or specialist book rarely beats holding alone in a rising period, yet it is what
  a portfolio needs (night 8's short specialist: 1.22 against holding's 0.10 on 2026, 0.07 against 1.00 on the unseen
  coins).
- **O. The holdout opens (proposed, for the operator's review):** for the first combination version that holds, by rule
  H, on the unseen coins and on both unseen dates; its record is written before the opening (the version, its commit,
  the measures expected); the result is recorded whatever it shows; from then the combination card is frozen for that
  holdout. A later version is judged on data that comes after the holdout (time passes), never on the holdout again.
  Why: the opening is then decided by the record, not by a choice; one look, so the result keeps its meaning.

## The stage moves (proposed: each move by a written rule, never by a person)
| From | To | The rule that moves it | Who runs it |
|---|---|---|---|
| an idea | a backtest and its verdicts | `select_next`'s order (one score) | the loop |
| confirmed (step 5) and profitable (step 6) on the folds | the unseen dates and the unseen coins tests | automatic (`run_idea` calls `unseen_test`; the unseen coins to be added) | `run_idea` |
| a book with its tests | a combination candidate | the combination card's rule 2 (admit); A2 may widen it to confirmed books failing step 6 on Calmar alone | the batch run (A7) |
| the candidates | a portfolio version | the combination card's rules 1 to 5 | the batch run (A7), after the morning merge |
| a portfolio version | the development judge's verdict | rule 6 on the unseen coins; rule H (C1) for the portfolio | the batch run (A7) |
| a version that holds | the sealed holdout | rule O | the batch run (A7), once |

## What this card does not do
It does not change a stage's own rule (each stays in its card); it does not open the holdout (rule O does, once).

## Open (for the review)
1. Rule H's comparison with holding, for the portfolio: on Sharpe (proposed), or on the yearly return.
2. Rule O: the unseen dates are already used by P4 and P10b; is "holds on both unseen dates" still a fair gate, or the
   unseen coins alone?
3. Does a later version need the unseen coins kept unused by any choice (today: no choice reads them)?
