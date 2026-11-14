# Exercises 7 and 8: reading (the same file is in exercise_8)

Two changes from exercise 6's reading:
- **The prompt:** "A config is not close if it drops the comparison or the condition the idea is about."
- **The request:** the two references moved to the start of the request, to cut the cost.

Exercises 7 and 8 are two runs of the same prompt on the same seven ideas, opus. No config was run by the engine.

## Against the card's criteria

| Criterion | Exercise 7 | Exercise 8 |
|---|---|---|
| Untestable where it should be | 2 of 2 (004-01 another coin; 005-01 no component recalls RSI at an earlier high) | 2 of 2 (005-01: "the closest composition ... drops that peak-to-peak comparison") |
| `Forecast` line matches the config | 5 of 5 | 5 of 5 |
| `standardise` first; graded; regime only for a condition; no constant inside a regime | 5 of 5 | 5 of 5 |
| Same side as the idea | 5 of 5 | 5 of 5 |
| Settings stable: RSI 14, SMA 50/200 | 5 of 5 | 5 of 5 |
| One horizon; one main measure plus one check; a number; no overlap; counts the data can give | 5 of 5 | 5 of 5 |
| Deviation stated | 5 of 5 | 5 of 5 |

No fault in either run. The divergence idea is untestable in both, and both answers name the missing comparison: the new line is used as written. Over exercises 4 to 8, the divergence idea was untestable in 4 of 5 runs. The one exception is exercise 6, before this line.

**Small differences between runs, all allowed:**
- The order of `signed_power` and `clip` differs in 001-01. The result is the same: the sign is kept, and the short side is kept.
- 003-01 gates low volume once with a rule on the low-volume up bar (exercise 7) and once with a veto on a volume filter (exercise 8).
- The two RSI plans recover the RSI from the recorded indicator value ("RSI = 50 − value / 0.4"). They use the record as change C intended.

## Cost

- **Exercise 7:** 1.81 USD. Moving the references to the start of the request did not help: each idea still cost 0.22 to 0.28. The model's cache did not reuse the shared start of the request across different ideas.
- **Exercise 8:** 0.34 USD, only because its requests were identical to exercise 7's, sent minutes earlier. That is not a saving a real run would get.
- **Probe** (`cache_probe/`): the references moved into the system prompt, two different ideas called in a row. The first cost 0.26 USD, the second 0.07. Both configs are the same as in exercises 7 and 8.
- **The helper now puts the references in the system prompt.** With that, a batch of ideas costs about 0.26 for the first idea and about 0.07 for each one after it. The content is the same; only its place changed. This change came after exercises 7 and 8, so the next real run should confirm the cost.

## Status

Exercises 7 and 8 are two clean exercises in a row. The card's "done when" is met.
