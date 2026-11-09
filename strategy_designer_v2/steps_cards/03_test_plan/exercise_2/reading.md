# Exercise 2: reading

Same seven ideas, references and script as exercise 1. Three prompt changes, from exercise 1's reading: name one horizon in bars; say which results are inconclusive (a new `inconclusive:` line); no constant inside a regime. Fourteen calls, none refused. Cost: opus 1.77 USD, sonnet 0.87 USD.

No config was run or validated by the engine: this is my reading against the guide and the catalogue.

## What the three changes did

| Change | opus | sonnet |
|---|---|---|
| One horizon, in bars | 6 of 6 (5, 5, 20, 1, 1, 10 bars) | 6 of 6 (5, 5, 20, 20, 5, 10 bars) |
| An inconclusive line | 6 of 6 | 6 of 6 |
| No constant inside a regime | held: 005-01 no longer uses one | held (none in exercise 1 either) |

All three worked on the first try. The "several horizons in one criterion" fault of exercise 1 (4 of 12) is gone.

## The configs

| | opus | sonnet |
|---|---|---|
| `standardise` first | 6 of 6 | 6 of 6 |
| Every strategy component graded | 6 of 6 | 6 of 6 |
| Regime only when the idea is a condition | 003-01 only (a veto on the low-volume up bar; valid) | 003-01 only (a rule on the same component) |
| Same side as the idea | 5 of 6: 005-01 also goes long on the mirror case, declared | 3 of 6: 002-01 and 002-05 keep the short side (as in exercise 1), 005-01 as opus; all declared |

**Stable across exercises.** Opus wrote the same config as in exercise 1 for four ideas (001-01, 001-03, 002-01, 002-05); it changed 003-01 (rule to veto) and 005-01 (dropped the constant). Sonnet's side change on the cross ideas is also stable: it is a habit, not noise.

## The criteria

- **Every criterion names what to measure, the horizon, the comparison, and the three outcomes.** They read as real test plans now.
- **The bar of evidence differs from plan to plan.** Opus asks for t ≤ -2 (001-01, 003-01), "more than one standard error" (001-03), "2 standard errors on non-overlapping blocks" (002-01), p < 0.05 by block bootstrap (002-05), 5 % (005-01). Sonnet mostly writes "clearly" without a number. Each is fixed before the data, so none is a fault against the prompt, but two ideas can now pass on different standards.
- **Overlapping returns.** Opus handles them in two plans (non-overlapping blocks, block bootstrap); sonnet names the problem in one inconclusive line. Elsewhere the 5-, 10- and 20-bar returns overlap and nothing says how that is counted.
- **The prompt's examples.** "Gains grow with position size" appears in 2 of 6 opus criteria and 6 of 6 sonnet criteria. Opus now fits the criterion to the idea; sonnet still applies the example everywhere.

## Still open from exercise 1

1. **The divergence idea (005-01) is forced again by both models**, now as an ungated sum (where the close sits in its range, minus RSI), symmetric, with a declared deviation. Two exercises, four forced answers: the prompt's "do not force it" does not stop it. It needs your ruling: accept a declared approximation, or require "untestable".
2. **002-01 and 002-05 are the same test** (opus: identical configs; sonnet: the same component, windows 200 and 250). Only the horizon and the criterion differ. This goes back to step 2 with the one-coin rule.

## Models

- **Opus:** same side as the idea in 5 of 6, stable configs, criteria with a stated bar of evidence and attention to overlapping returns. 0.25 USD per idea.
- **Sonnet:** follows the rules, but changes the idea's side on the cross ideas in both exercises, and writes "clearly" where a number is needed. 0.12 USD per idea.

## Recommendation

Opus. Two decisions before exercise 3:
1. The divergence ruling (above).
2. Whether the bar of evidence is left to each plan, or fixed in the prompt in one sentence (for example: "state the evidence you require as a number, and count overlapping returns once"). The second keeps the plans comparable without choosing the measure for the model.
