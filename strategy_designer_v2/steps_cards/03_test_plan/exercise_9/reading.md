# Exercises 9 and 10: reading (the same file is in exercise_10)

The helper as it now stands:
- the two references are in the system prompt;
- a plan is named after its idea and its bar size (`NNN-KK_short-name_1d`);
- each plan gets a line in the plans folder's `INDEX.md`.

The prompt is unchanged since exercise 7. Two runs on the same seven ideas, opus. No config was run by the engine.

## Cost

- Exercise 9: 0.36 USD for seven ideas.
- Exercise 10: 0.30 USD.

That is 0.01 to 0.08 USD per idea, against about 0.26 when the references were in the request. Even the first call of each run was cheap: the system prompt was already in the cache from the run just before. A first call after more than an hour without one would cost about 0.26, as in exercise 8's probe.

## Against the card's criteria

`helper/check_plans.py` checks the parts that can be checked by code:
- **in the config:** `standardise` first; no on/off class or dead-zone op in a strategy; no constant inside a gated regime; no `vol_target`;
- **in the criterion:** a horizon, a number, non-overlapping returns, a supporting check, an inconclusive line, no "fading".

All ten testable plans pass. (Its first version missed "a t-stat of -2 or lower" as a number; the regex is fixed.) I read the rest by hand.

| Criterion | Exercise 9 | Exercise 10 |
|---|---|---|
| Untestable where it should be (004-01, 005-01) | 2 of 2 | 2 of 2 |
| Same side as the idea | 5 of 5 | 5 of 5 |
| Settings stable: RSI 14, SMA 50/200 | 5 of 5 | 5 of 5 |
| Regime only for a condition (003-01, a rule on the low-volume up bar) | 5 of 5 | 5 of 5 |
| Deviation stated | 5 of 5 | 5 of 5 |

**No fault in either run.** The configs are the same in both, up to the order of `negate`, `clip` and `signed_power`, which gives the same forecast.

## Status

Exercises 9 and 10 are two clean exercises in a row, on the final helper. With exercises 7 and 8, that makes four clean runs in a row since the "not close" line was added.
