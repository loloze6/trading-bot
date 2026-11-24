# Topic 31: Choosing and judging an idea on different data (folds)

Status: open  
Where: research: step 7, step 5, the folds  
Opened: 2026-11-19 (operator, from topic 30)

## Question
Should the years an idea is chosen on differ from the years it is judged on, to keep its verdict honest?

## Seen
- Every idea is backtested on folds A to D (about 8 years, 24 windows): the default since step 3's exercise 26; before,
  fold A alone (2 years), where t = 2 needed an annual Sharpe of about 1.4 (`03_test_plan/card.md`).
- Step 7 reads an idea's record on folds A to D and proposes its children; step 5 judges them on the same folds. 7.g
  picks, for example, the best hour of the day in the record: judged on the same years, its t is flattered (topic 30).
- The only data never used to choose: the unseen periods (2016-17, 2026), run at the end for profitable ideas only
  (topic 20).
- No design of folds varying per run is found in this workflow's cards, run briefs or commits.

- **The fold reduction's impact, measured (2026-11-24, the operator; `47_review/folds_power.py`, `folds_power.csv`):** the
  idea's size and its day-clustered t (the verdict's bar t >= 2) recomputed for the 277 confirmed books of the register
  on all four folds and on every subset of 3, 2 and 1 folds. Of the 125 books sure on 8 years, sure again on 6 years
  71 %, on 4 years 49 %, on 2 years 25 % (daily books 69, 47, 24 %; hourly 76, 54, 30 %); median t 1.77, 1.61, 1.34,
  0.95, close to the square root of the years (0.87, 0.71, 0.50 of the 8-year t). So halving the years halves the
  confirmations of real effects: the reason all four folds were adopted holds. But the direction survives: of the books
  sure on 8 years, the effect keeps its sign on 6 years in 100 %, on 4 years in 99 % (t >= 1: 87 %), on 2 years in 93 %.
  A check of the sign on the 2 folds the analyst did not see would cost almost no real effect.

- **Three rules tested on past ideas (2026-11-24, the operator: "test the best 3 in parallel"; `47_review/fold_rules_test.py`,
  `fold_rules_test.csv`; no model call):** the 271 confirmed follow-ups with a register record, 62 of them tested on the
  unseen dates. T1, the effect points its own way on the newer folds (2022-25): keeps 82 %; holds on both unseen periods
  46 % kept, 62 % removed (8 tested). T2, a higher bar for the cases step 7 compared (median 98 rows seen per analysis,
  so a bar near t 3.5): keeps 45 %; holds 33 % kept, 39 % removed. T3, both: keeps 39 %; holds 27 % kept, 42 % removed.
  None keeps the ideas that hold better than those it removes; the samples are small (8 to 19 removed ideas tested),
  and T1 is weaker in retrospect than live (step 7 saw the newer years). The net lean does not explain it either: the
  long-leaning follow-ups held more often (61 %, 36 tested) than those with no lean (35 %, 23). Reading: on past
  evidence, no fold rule tried predicts which ideas hold on the two short unseen periods; nor did in-sample strength
  (topic 47, 1d-11). No change to the folds on this evidence.

## Why it matters
A verdict on the years an idea was picked from can be partly luck; it would show as profitable ideas failing on unseen
dates.

## Options
| Option | Gain | Risk |
|---|---|---|
| Keep folds A to D for all (as today) | the largest sample; results comparable across runs | choice and judgement on the same years |
| Different folds per run | each run sees other years | inside a run, choice and judgement still share the years; runs not comparable (select_next's records) |
| Choose on some folds, judge on the others | an honest verdict | half the sample, the reason all four folds were adopted |
| On 1h, fewer folds | faster | fewer kinds of market (crashes of 2018 and 2022, two bull markets); step 6 needs years |

Recommended: no change now. After topic 30's change 1, read the unseen test of the profitable ideas it brings: if many
fail there, the split becomes worth its cost.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-19 | Noted; no change to the folds now | operator's ok, on the design session's proposal | the years still matter on 1h (markets, profitability); the unseen test shows first whether choice bias bites | fewer folds on 1h; folds per run |

## Status and next
Open. Read again once change 1 has produced profitable ideas and their unseen tests.

## Links
Topics 20, 30; `03_test_plan/card.md`; `common/unseen_dates.md`.
