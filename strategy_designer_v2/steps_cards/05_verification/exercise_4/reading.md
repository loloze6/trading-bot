# Exercises 3 and 4: reading

**What changed since exercises 1 and 2:**
- conventions for open details in `record_description.md` (the non-overlapping grid, which t-test, the order of a difference);
- the measure's value and its statistic are separate, and "counts" names every count.

The same 29 plans, opus, two runs. Cost: 1.30 USD and 1.04 USD. One function was refused, once, in run 4 (its counts were not a dict of numbers); the retry passed.

**A bug, found and fixed.** In both runs, `verdict.md` showed the placeholder text instead of "decided by" and "reading", because my last code edit dropped an `f` from a format string. The values were intact in `result.json`. The verdict files were rewritten from them with the fixed code, with no new model call.

## Agreement between the two runs

| | Exercises 1 and 2 | Exercises 3 and 4 |
|---|---|---|
| Same status | 14 of 15 | 14 of 15 |
| Same main value and statistic | 10 of 15 | **13 of 15** |

- **`001-03`, which flipped before, is now stable:** rejected twice, on the same 42 cases. The non-overlapping convention settled it.
- **`003-03` now flips: rejected in run 3, inconclusive in run 4.** The plan says the return is "weighted by the position":
  - Run 3 took the mean of position × return: -0.0007, so rejected (≤ 0).
  - Run 4 took the weighted mean, Σ(position × return) / Σ(position): +0.0003, with a supporting check of the other sign, so inconclusive.

  A convention is added for exercises 5 and 6: "a mean weighted by X is sum(value × X) / sum(X)".
- **`003-05`:** the same status, but different cases. Run 3 drops bars whose move is not up (145 thin and 120 heavy cases); run 4 keeps every labelled bar (211 and 146). The plan does not say. This is a fault of the plan, to settle in step 3, like the other open details.

**`counts` sometimes held more than counts** (means, rates). Added for exercises 5 and 6: "counts holds counts only".

## Status

Not met: one status still differs between two runs. Exercises 5 and 6 run with the two additions above.
