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
