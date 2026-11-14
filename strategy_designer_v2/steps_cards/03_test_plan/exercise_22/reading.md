# Exercises 21 and 22: the two fixes, final form (the same file is in exercise_21)

**Prompt change from exercise 19.** The equivalence line is replaced by: "A result near zero is never a reject, even when the idea or its brief says it is wrong if there is no difference: it is inconclusive." The extremes line is kept.

The 13 fixed ideas, opus, two runs side by side. Cost 0.81 and 0.87 USD. No code refusal.

| | Exercise 21 | Exercise 22 |
|---|---|---|
| Outcomes | 6 plans, 1 untestable, 6 missing-components | the same |
| Rejects that need t of 2 or more against the idea | 6 of 6 | 6 of 6 |
| "Near zero" rejects | 0 | 0 |
| RSI-extreme plans with exponent 3 | 2 of 2 | 2 of 2 |

**Both fixes hold in both runs.**

**One plan is not clean, in both runs: 003-07 (quiet-hours moves revert).** Exercises 15 to 18 all marked its situation *replaced* (daily bars cannot show quiet hours, and no component reads the weekday), so it was refused. Here the fidelity line restates the idea's situation as "a sharp move while volume is low", dropping "quiet hours or weekends" from the idea's own words, and marks it *adapted*. The test becomes "low-volume days revert", a plan. That trims the idea to fit the vessel: the fidelity is not honest, which the criteria forbid.

**Status.** "Done when" is not met: 003-07 fails "fidelity is honest" twice. The cause is not in the two fixes (they do not touch the situation line); it may be variance that happened twice. A general line would prevent it: state each part of the idea in its own words, without dropping any of its conditions. Proposed to the operator, not made.

`check_plans.py`: two "overlapping returns" flags (003-07, 002-05), both 1-bar horizons: false alarms.
