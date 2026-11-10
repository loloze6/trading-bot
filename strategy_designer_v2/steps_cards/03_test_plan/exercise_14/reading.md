# Exercises 13 and 14: reading

**What changed.** The fidelity rule and the three outcomes:
- The idea is split into situation, comparison and outcome. Each part is kept, adapted (only as the config's logic forces) or replaced, followed by the verdict transfer.
- There are three outcomes: plan, untestable, missing-components.
- The plan file is now structured.
- The two lines that named single cases are gone.

**Inputs.** The 13 fixed ideas: the 7 earlier ones, the 5 other divergence ideas, and 003-07 (quiet hours) from step 2, exercise 4. Opus, two runs. Cost: 0.97 USD and 0.66 USD. No config was run by the engine.

## Outcomes, the same in both runs

| Idea | Expected | Exercise 13 | Exercise 14 |
|---|---|---|---|
| 001-01, 001-03, 002-01, 002-05, 003-01 | plan | plan, fit adapted (5 of 5) | the same |
| 004-01 altcoins follow bitcoin | untestable | untestable: two coins | the same |
| 005-01 to 005-06 RSI divergence | missing-components | missing-components (6 of 6) | the same |
| 003-07 quiet-hours moves revert | missing-components (my expectation) | **untestable** | the same |

**003-07: the model is right, and I was wrong.** On daily bars, a bar holds a whole day, so quiet hours are not in the data at all. It is untestable on 1d. On hourly bars it would be missing-components (the bar's hour is in the data, but no component reads it). This is not tested yet.

**No refusal by the code** in 26 calls. Every plan's fidelity agrees with its outcome.

## Quality

- **Fidelity is honest.** In the plans, the situation is "adapted" (a threshold made graded) and the outcome is "adapted" ("while" instead of "after") or "kept". In the divergence refusals, the comparison is "replaced: no component recalls RSI at an earlier high", with the verdict transfer "no".
- **The wish list is concrete.** For example, "RSI at the previous swing high minus RSI now, from closes, graded". Different ideas propose overlapping components (for example "RSI position in its own range" appears several times). Grouping them is a later task for the operator.
- **The fit is "adapted" for every plan.** None is exact, because every idea's situation is a threshold the config makes graded. As expected: "exact" will be rare.
- **The plans are the same as before.** Same configs, same sides, same settings.

## One fault against the operator's requirement: length

The operator asked for the fidelity to be reflected concisely. It is not:

| | Fidelity line, words (median / max) | Criterion line, words (median / max) |
|---|---|---|
| Exercise 13 | 42 / 95 | 47 / 129 |
| Exercise 14 | 40 / 110 | 45 / 121 |

The prompt said nothing about length. One line is added for exercises 15 and 16: "Keep every line short: each fidelity line is one short sentence, and each criterion line one or two". The output template also asks for each part "in a few words".

## Status

The outcomes are right and stable in both runs, but both runs fail the conciseness requirement. Exercises 15 and 16 run with the line added.
