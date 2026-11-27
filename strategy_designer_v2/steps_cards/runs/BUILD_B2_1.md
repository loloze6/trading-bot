# Build B2.1: a run has a target box and stays in it (2026-11-27, branch `build-b2-1`)

## Purpose (written before the build)
Next steps B2.1 (the operator's go, 2026-11-27): each run searches where the portfolio lacks strategies. A run gets a
target box (a market profile and a side), chosen by one rule from the profile map or given by the operator; line 7.g
looks there first; the loop tests in the run only the ideas acting in the box.

## Expected outcomes (written before the build)
1. **The rule on today's map:** the designer expects rising agitated (long or short) first: no idea names it exactly,
   and it is the profile with the largest share of market days or close to it. A box with no exact strategy and a
   larger share would come first instead; the table says which.
2. **The filter on night 9's six runs** (each with its run's header box): most of B's, E's and F's tested ideas kept;
   F's left-out share near night 9's reading (17 of 28 outside); some profitable ideas left out (B's four 074 "bounce
   in a falling market fades" were off its choppy box).
3. **A run without `--target-box`:** the same files as before, the allowed differences being times, shas, run ids and
   the order in which parallel lines finish (as `BUILD_A4_JOIN.md`).
4. Both test suites pass.
