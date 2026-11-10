# Exercises 11 and 12: reading

**Prompt change, from the plans review.** Four of the twelve divergence plans in `plans/` were forced. One line was added after "a config is not close if it drops the comparison or the condition the idea is about":

> The config has no memory of past turning points: an idea that compares a value now with its value at an earlier high or low cannot be built, and is untestable.

**Inputs.** The seven fixed ideas, plus the five other divergence ideas of step 2, exercise 3 (005-02 to 005-06), all on daily bars. Opus, two runs. Cost: 0.67 USD and 0.37 USD. No config was run by the engine.

## Results

| | Exercise 11 | Exercise 12 |
|---|---|---|
| Divergence ideas untestable (005-01 to 005-06) | 6 of 6 | 6 of 6 |
| 004-01 untestable (another coin) | yes | yes |
| Five testable plans: `check_plans.py` (hard rules, the criterion's parts) | 5 of 5 | 5 of 5 |
| Five testable plans: same side, same settings as exercise 10 | 5 of 5 | 5 of 5 |

Every untestable answer names the missing piece: RSI at the earlier high or low. The five testable configs are the same as exercise 10's, up to the order of `negate`, `clip` and `signed_power`, which gives the same forecast.

## Status

Exercises 11 and 12 are two clean exercises in a row with the current prompt. The new line adds a case (divergence) and changes nothing else.
