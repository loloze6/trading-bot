# Exercises 19 and 20: the two approved fixes, first form (the same file is in exercise_19)

**Prompt changes** (approved: "Fix ok").
- **Extremes:** "If the idea's situation is a rare extreme, the position away from the extreme should be close to zero: use the strongest graded dead zone the guide allows."
- **"No difference":** a reject on "no difference" allowed only as an equivalence test: the whole 90 % confidence interval inside a band fixed in the plan.

The 13 fixed ideas, opus, two runs side by side. Cost 0.86 and 0.83 USD. Outcomes: 5 plans, 2 untestable, 6 missing-components, both runs, as in exercises 17 and 18.

**Extremes: works.** Both RSI-extreme plans (001-01, 001-03) now use `signed_power` with exponent 3, the strongest the guide allows, in both runs (exponent 2 before). The other plans are unchanged.

**"No difference": not stable.** The equivalence reject was used, but its band is a number the model picks, and it changes between runs: 001-03 ±1.0 % in one run and ±0.5 % in the other; 002-01 ±0.5 % in one and ±2 % in the other (with a different horizon). 001-01 uses it in one run only. A reject would depend on an invented number. Any fixed band would be a cost ("too small to trade"), which is step 6's question. Replaced in exercises 21 and 22 by the simpler rule.
