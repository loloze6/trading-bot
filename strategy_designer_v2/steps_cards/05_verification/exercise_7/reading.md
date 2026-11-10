# Exercise 7: the situation check

**What changed.** The function now checks, before measuring, that the config's forecast is active on the bars of the plan's situation and on the side the idea expects. It reads the plan's Fidelity lines and the record's raw indicator values. Below 90 % agreement, the status is "mismatch". This was run on today's plans and records, which were made before the symmetric criteria. Opus, one run. Cost: about 1.4 USD.

## What the check found

| Plan | Agreement | Status |
|---|---|---|
| 13 plans | 100 % | verdict as before |
| `002-02` down-cross drift | **0 %** | **mismatch**: the config goes short when SMA50 is *above* SMA200, the opposite of its Fidelity line ("while SMA50 is below SMA200"). This is the fault found by hand in exercise 6's review. |
| `003-05` up-move retrace by volume | **19 %** | **mismatch**: the plan's situation is a top-decile up move, so about 10 % of bars. The config is active on 365 of 730 bars. The percentile vetoes in the regime detector do not select what the plan says. Nobody had seen this. |

**Both mismatches are real config faults, and there is no false alarm:** every correct plan scores 100 %. Before the check, these two plans gave a "rejected" and an "inconclusive" verdict about tests that were not their idea.

## Not changed by this exercise

These plans still have the asymmetric criteria. Three of the four rejections (`001-03`, `003-01`, `003-04`) rest on t between -0.76 and +0.07; `002-04` is the fourth. The plans are rewritten next, with the symmetric rule.
