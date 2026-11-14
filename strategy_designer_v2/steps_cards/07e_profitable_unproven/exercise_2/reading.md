# 7.e exercise 2: real inputs, ideas taken through the workflow, final review (2026-11-14)

**Inputs** (backtested with the current steps, sizing included): the 002-03 repair from 7.d (profitable: Sharpe 0.95,
Calmar 0.92; idea inconclusive, t 0.61) and N2-04, slow and fast momentum (profitable: Sharpe 1.06, Calmar 1.22; idea
inconclusive, t 0.85). N2-06 (Calmar 0.742, not profitable): the line did not run, as its entry condition says.

**Two runs on each** (`run_1/`, `run_2/`, 1.43 USD). Both inputs, both runs, the same cause: the book earns from the
idea, but at a shorter horizon than the plan's 20 bars (002-03: t 3.10 at 1 bar, 2.88 at 5, 2.64 at 10, 0.94 at 20;
N2-04: next-day return 0.29 % in the market against 0.03 % out, t 3.21). Also found: being above the 200-day average
adds nothing by itself (002-03 run 1 F3); the sizing shifts the gain to calm periods (N2-04 run 2 F7).

**The ideas through steps 3 to 6:**

| Idea | Step 3 | Step 5 | Step 6 |
|---|---|---|---|
| 002-03 e1: above the long average, the nearer the recent high and the stronger the recent rise, the larger the return over the following days to two weeks | plan (10 bars) | **confirmed** (Welch t 2.20) | profitable (Sharpe 0.95, Calmar 0.92) |
| N2-04 e1: 60-day and 20-day returns both up, the next few days rise more than usual | plan (5 bars) | **confirmed** (t 2.22) | profitable (Sharpe 1.06, Calmar 1.22) |

Both meet the line's relevance test (the idea of what the book earns from is confirmed); both now meet 7.f's entry.

**Final review**, two fixes:
- the prompt looked only for a gain from something else than the idea; both runs found a gain from the idea measured
  at the wrong horizon. Both causes are now named (another source; or the idea measured elsewhere: horizon,
  comparison, side);
- "is the gain the market's own rise?" had no shared definition, and two runs read the same numbers in opposite ways;
  `common/measures.md` now defines the market part (position x the coin's mean return) and timing (the rest).

**Confirming run** (`run_3/`, 0.70 USD): both analyses name the horizon cause in their first findings, both use the
shared split (002-03: timing 0.00034 against market 0.00022 a day), the same main idea recurs. To watch: one idea
(N2-04 run 3 e3) names "years when the coin trends up over the year", which read literally uses the year's outcome.
