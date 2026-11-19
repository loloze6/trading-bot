# Topic 04: Record the regime detector's values in the backtest

Status: open  
Where: research: engine  
Opened: 2026-11-13 (overnight run; step 5's false mismatch on N1-01)

## Question
Can steps 5 and 7 read the regime detector's measures from the backtest record instead of recomputing them?

## Seen
- The engine records the strategies' components, but of the regime detector only its decision (the `regime`
  column). Steps 5 and 7 must recompute the detector's measures from prices; step 5 once read a false mismatch (N1-01).
- Also in the record (2026-11-19): `forecast_distribution.csv` puts a forecast of exactly 0 in the bin "-5_0" (bins
  closed on the right), so its "negative" bins count the flat bars. Read the bars for the sign.

## Why it matters
A recomputation can differ from what the engine used, and step 5 then judges the wrong thing.

## Options
| Option | Gain | Risk |
|---|---|---|
| Record the detector's value and each of its components' values | steps read what the engine used | shared code: proof needed |
| Leave it | no work | recomputation errors stay possible |

Recommended: record them (shared code, with its proof), when opened.

## Decisions
None yet.

## Status and next
Opens when the operator says so.

## Links
`common/backtest_record.md`.
