# Exercises 15 and 16: reading (the same file is in exercise_16)

**What changed since exercises 13 and 14:** one line on length. "Keep every line short: each fidelity line is one short sentence, and each criterion line one or two." The output template also asks for each part of the idea "in a few words". Same 13 ideas, opus, two runs. Cost: 0.92 USD and 0.56 USD. No config was run by the engine.

## Outcomes

The same as in exercises 13 and 14, in both runs:
- 5 plans (fit adapted);
- 004-01 and 003-07 untestable;
- 005-01 to 005-06 missing-components.

`check_plans.py`: every plan passes the hard-rule and criterion checks, and every refusal has its fidelity and its reason.

**The consistency check worked once.** In exercise 15, the first answer for 005-06 was missing-components, but its fidelity had no replaced part and a "yes" verdict transfer. The code refused it as a contradiction, and the second answer was consistent. Without the check, a refusal would have contradicted its own fidelity.

## Length

| | Fidelity line, words (median / max) | Criterion line, words (median / max) |
|---|---|---|
| Exercises 13, 14 (before) | 40 / 110 | 46 / 129 |
| Exercise 15 | 24 / 37 | 30 / 62 |
| Exercise 16 | 24 / 39 | 28 / 55 |

Fidelity lines are about 40 % shorter, with no line over 40 words. Example, exercise 16, 005-01:

```
- Situation: price closes at a new recent high -> kept: DonchianBreakoutComponent gives +sf when the close is the highest of its window.
- Comparison: RSI now is below RSI at the previous price high -> replaced: no component stores RSI at a past price pivot, and RSI rank against its own history is a different quantity.
- Outcome: price falls and retraces part of the run-up -> adapted: a negative forecast sized by divergence strength, judged over a fixed horizon.
- Verdict transfer: no: without RSI measured at the previous price high, the test would judge "high price with weak RSI", not divergence.
```

## Status

Exercises 15 and 16 are two clean exercises in a row with the fidelity rule, the three outcomes, and the structured, concise output. The card's "done when" is met.
