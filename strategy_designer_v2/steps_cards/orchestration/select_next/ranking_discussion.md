# The ranking of the next idea: for the operator's decision (2026-11-17)

## The problem, in one line
The score picks variants of an idea that already worked before the other ideas of the same theory, so a run tests one
lineage deeply and leaves the rest of the theory untested.

## How the score works today (`select_next`)
score = record of the line that wrote the idea / (1 + generation). A line's record is its share of analyses that led to
a confirmed or profitable idea, over all runs: 7.e 0.71, 7.c 0.67, 7.g 0.65, 7.b 0.60, 7.d 0.45, 7.a 0.25, and
**step 2 (a brief's own ideas) 0.09** (0 of 9: a brief's first ideas rarely confirm; the lines refine them).

## What it did, measured
| Run | Turns | Turns taken by one lineage (a brief idea and the ideas that came from it) |
|---|---|---|
| night_run | 30 | 26 (011-01, weekend reversal); brief 010's 4 ideas ranked below its third generation (0.17 against 0.18) |
| night_013_run | 33 | 28 (013-01, near the high) |
| night_rsi_run (test 1) | queue now | 010-01's 7 child ideas (0.15 to 0.23) ahead of the 7 other RSI brief ideas (0.09), just unblocked |

A brief idea scores 0.09 whatever its theory, because step 2's record is low; a child of a line scores 0.15 to 0.33. So
a new theory's ideas always wait behind the variants of the first idea that worked.

## Options
| | Rule | Gain | Cost or risk |
|---|---|---|---|
| **A. Brief ideas first** | a run tests every idea of its briefs (generation 0) before any idea a line proposed; then the score, as today | every idea of a theory is tested once; simple, one rule | the lines' leads wait until the brief's ideas are done (a brief has 4 to 8 ideas) |
| B. Lineages in turn | each turn goes to the next lineage that has a candidate (in rotation); within it, the best score | no lineage takes the whole run; depth and breadth balanced | weak lineages get as many turns as strong ones (cost) |
| C. Count an effect once | a line's record counts a success once per effect, not per variant (needs to tell two ideas are the same effect) | rewards finding new effects | needs a similarity rule (topic 5): complex |
| D. Stronger generation discount | score = record x 0.5^generation | fewer deep variants | a tuned number; step 2's 0.09 still loses to a 7.g child (0.33) |

## Recommendation: A
It is the simplest rule that answers the problem seen three times: every idea of a theory gets one test before the
workflow goes deep on one of them. The score is kept as it is for everything after. B can be added later if one lineage
still takes most of a run once the brief's ideas are done (night_013_run would show it: its other brief ideas were
blocked, so A alone would not have changed it there; now that blocked ideas are unblocked by the components step, they
would be tested first).

## What A changes
`select_next`: candidates of generation 0 come first, ranked by the score among themselves; then the others, by the
score. Its card and a test. The loop and the steps unchanged. Proof: the ranking of the 11 runs today, old against new:
only runs with untested brief ideas change order.
