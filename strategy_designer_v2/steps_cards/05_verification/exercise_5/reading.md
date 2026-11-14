# Exercises 5 and 6: reading (the same file is in exercise_6)

**What changed since exercises 3 and 4:** two conventions in `record_description.md`:
- a mean "weighted by" X is sum(value × X) / sum(X);
- `counts` holds counts only.

The same 29 plans, opus, two runs. Cost: 1.31 USD and 0.91 USD. No function was refused.

## Agreement between the two runs

| | Exercises 1 and 2 | Exercises 3 and 4 | Exercises 5 and 6 |
|---|---|---|---|
| Same status | 14 of 15 | 14 of 15 | **15 of 15** |
| Same value and statistic | 10 of 15 | 13 of 15 | 13 of 15, plus 2 cosmetic |

The two cosmetic differences:
- **`002-06`:** the same value, written once as a percentage (-0.0578) and once as a fraction (-0.000578), with the same t (-0.313).
- **`003-03`:** the same value, and a t that differs in the fifth decimal (-0.24884 against -0.24881).

## The verdicts

| | count | plans |
|---|---|---|
| confirmed | 0 | |
| rejected | 6 | 001-03, 002-02, 002-04, 003-01, 003-03, 003-04 |
| inconclusive | 9 | 001-01, 001-02, 001-04, 002-01, 002-03, 002-05, 002-06, 003-05, 003-06 |
| no verdict | 14 | 7 untestable, 6 missing-components, 003-02 (refused by the engine) |

On the default data (BTC, plus ETH for the RSI ideas; daily bars; fold A), no idea is confirmed. The many inconclusive verdicts mostly come from small samples: 13 to 60 non-overlapping cases, against thresholds of t ≥ 2. The card's open point on the default data foresaw this.

## Status

Exercises 5 and 6 are two clean runs in a row, with the same status for every plan. The card's "done when" is met. Run 6, made with the current helper, is copied as the production verdicts into `../verdicts/`.
