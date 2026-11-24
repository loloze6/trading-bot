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
