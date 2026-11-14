# Exercise 4: reading

Opus only, the same seven ideas, one call per idea. Six changes from `../exercise_2/review_before_exercise_4.md`:
- **A:** write the exact forecast first; "untestable" if the config cannot come close.
- **B:** tell the model the data's windows.
- **C:** say what the record holds, and that a position lasts only while the forecast is not zero.
- **D:** one main measure, plus at most one supporting check.
- **E:** the evidence as a number, with overlapping returns counted once.
- **F:** code checks class and param names against the catalogue.

Cost: 1.83 USD for the seven ideas (0.22 to 0.28 each), plus 0.79 for three reruns. Exercise 2 cost 1.77. No config was run by the engine.

## Change by change

| | Change | Held? | What the output shows |
|---|---|---|---|
| A | exact forecast first | **yes** | Every plan opens with a `Forecast:` line that matches its config. **005-01 (divergence) is untestable**, with the right reason; it was forced in exercises 1 and 2. 004-01 is untestable, as before. |
| B | the data's windows | **yes, with a side effect, fixed** | The criteria now fit the data: "pooled over the 6 windows", "positive in at least 4 of the 6 windows", "at least 30 events". **Side effect:** opus believed warm-up eats into each 122-bar window. So it changed the averages from the 50/200 convention to 10/30 and 20/50, and wrote "about 36 bars of each window are lost to warm-up". In fact the engine loads warm-up bars before each window. One line now says so. In the rerun of the three affected ideas, the warm-up worry is gone. |
| C | the record, and no fading | **yes** | No "fading" in any plan. Criteria read the forward return after the signal bars, from the record. 003-01 measures the position times the next day's return. |
| D | one main measure plus one check | **yes** | 5 of 5 plans: "main measure" and "supporting check" are named, both short. |
| E | evidence as a number, overlaps counted once | **yes** | 5 of 5 give a number (t ≥ 2 in four; "+1.0 percentage point over at least 30 blocks" in one). 5 of 5 sample non-overlapping returns (every 5th or 10th bar, or 1-bar horizons). |
| F | class and param names checked | **nothing to catch** | No refusal; all names are in the catalogue. |

## The configs

- **Hard rules:** `standardise` first and graded strategy components, 5 of 5. Regime only for a condition: 003-01 (a veto on the low-volume up bar), as before.
- **Same side as the idea:** 5 of 5.
- **New:** 003-01 sets `strategies.min_allocation_change` to 0, "so that small shorts are opened and every short is closed the next day". It is a valid key (V11), and a sensible choice for a one-day test.

## What is still not right

1. **Settings for the moving-average ideas are not stable.** Run 1: 10/30 and 20/50, driven by the warm-up worry. Rerun: 20/50 for 002-01 ("a convention I chose") and 50/200 for 002-05. Both are conventions, but the same brief now gets two different pairs of averages. The prompt says "from convention or from the brief". For a daily moving-average cross there is more than one convention, so it does not fix the choice.
2. **The `Forecast:` line describes the config, not the idea's ideal forecast.** It uses component names. It still works, because the model checks the gap and says "untestable" when the gap is real (005-01). But it is not the plain-words, engine-free description the exercise 3 split produced.

## Against exercise 2 (one call, opus)

| | exercise 2 | exercise 4 |
|---|---|---|
| Ideas faked instead of untestable | 1 (005-01) | 0 |
| Criteria the data can support | not checked by the model | sized to 6 windows of about 122 bars |
| A number for the evidence | 4 of 5 | 5 of 5 |
| Overlapping returns counted once | 2 of 5 | 5 of 5 |
| One main measure | 0 of 5 | 5 of 5 |
| Cost per idea | about 0.25 | about 0.26 |

## Recommendation

Keep all six changes, plus the warm-up line. Two small points for exercise 5:
- When neither the idea nor the brief gives a setting, prefer the most common convention for the bar size, and use the same choice for ideas from the same brief.
- Exercise 5 should run on the same seven ideas, unchanged otherwise, to see whether the result is stable. With a clean result, this would make the first of "two exercises in a row".
