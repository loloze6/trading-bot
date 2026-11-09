# Exercise 3: one call or two? Reading

The same seven ideas, written in two calls instead of one:
- **Call 1** (opus, no reference documents, about 0.04 USD): the test plan in plain words. It gives the forecast (indicators, settings, sign, size), the criterion and the deviation, or "untestable".
- **Call 2** (with the two references): turns that plan into a config, and says what the config computes differently from the plan. It runs once with opus and once with sonnet, on the same call-1 plan.

The comparison is exercise 2, which did the same seven ideas in one call. No config was run by the engine.

## Cost

| | total, 7 ideas | per testable idea |
|---|---|---|
| One call, opus (exercise 2) | 1.77 USD | about 0.25 |
| One call, sonnet (exercise 2) | 0.87 USD | about 0.12 |
| Two calls, opus + opus | 1.97 USD | about 0.33 (0.05 + 0.28) |
| Two calls, opus + sonnet | about 1.06 USD (one call-2 cost lost in a crash, about 0.13) | about 0.18 (0.05 + 0.13) |

Call 2 costs more than the single call: it reads the references and the plan, and writes a long "differs".

## Quality

| | One call (exercise 2, opus) | Two calls (opus + opus) |
|---|---|---|
| Altcoins follow bitcoin (004-01) | untestable, right | untestable at call 1, right, and cheap (0.02) |
| RSI divergence (005-01) | **forced**: an approximation, declared | **untestable**, right, in both opus and sonnet. Call 1 wrote the exact divergence rule; call 2 saw that no component computes it |
| The plan matches the config | yes: the criterion is written for the config | **no, 5 of 5 configs differ from the plan's forecast.** Call 1 does not know what the engine can compute: it writes "short above RSI 70", "divide by the volatility of returns", "3-bar volume against the 20-bar median". Call 2 cannot build these, and builds something close instead: the short starts at RSI 50, the scale is the gap's own past size, and the volume test is on/off |
| The criterion measures what the config does | yes | **not always.** Example 001-01: the criterion looks at "bars where the forecast is not zero" and compares "RSI above 80 with RSI 70 to 80". The config is not zero from RSI 50, so the bars measured are not the bars the plan meant |
| Readability of the plan | good | **better**: exact formulas and thresholds in plain words |
| Config faults | 0 of 5 | 0 of 5 with opus. With sonnet: one config was not valid JSON (the real helper would retry; this test script did not), and the volume idea was marked untestable where opus built a gate. Sonnet's reason holds: thinness is graded in the plan and only on/off in the catalogue |

## Reading

- **What two calls win:** honesty about what cannot be built. When call 1 states the idea exactly, call 2 sees the gap and refuses to fake it. The divergence idea, forced four times in one call, is now untestable.
- **What two calls lose:** consistency. The plan is written for a forecast the engine cannot compute, so the config differs from it in every case. The criterion was written for the plan, not for the config, so the test and its criterion no longer match. This is the risk named before the test, and it happened.
- **Cost:** two calls cost more with opus (0.33 against 0.25 per idea), less with sonnet as call 2 (0.18).

## Recommendation

Keep one call, and borrow the one thing two calls do better. Ask, inside the single prompt: first write the forecast the idea needs, in plain words and exactly; then build the config; if the config cannot come close to that forecast, answer "untestable" rather than approximate. Same cost as one call, criterion written for the real config, and the honesty the split showed. To be tested in exercise 4, on the same seven ideas.
