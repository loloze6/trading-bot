---
line: 7.b inconclusive
backtest: 069-02.d3_below-high-up-day-two-day-fade_1d
idea tested: 069-02.d3_below-high-up-day-two-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2205 USD
---
## Findings
- **F1:** Step 5's result points the way the idea predicts but falls short of the bar. The unusual move is +0.25 % per case over 2 days with t 1.49, over 4528 cases on 1594 days, a strength of only 0.037 of a usual 6.58 % move. On folds B and C, up days on the 2-day grid show a similar short-side excess of +0.18 % (t 1.05, n 1835), and non-up days show −0.25 % (t −1.46, n 2178). The sign is right, but the effect is small against the coin's own swings.
- **F2:** Almost all of the effect sits in the deepest fifth of up-day closes below the 20-day high. At 2 days that fifth gives a short excess of +1.35 % (t 2.79, n 367), against +0.15 %, +0.33 %, −0.49 % and −0.45 % for the other four fifths. The same split holds at 1 day (+1.02 %, t 4.69, n 734), at 3 days (+1.52 %, t 2.41, n 243) and at 5 days (+2.34 %, t 2.07, n 129). So the grading lives in the tail and is not linear, which leaves the overall mean weak (correlation of depth with the 2-day excess −0.073).
- **F3:** The effect is not steady over time, and much of it is drowned by the market's own moves. By year, the 2-day short excess runs +1.40 % (t 3.51) in 2018 and +0.48 % (t 1.80) in 2019, then −0.53 % (t −1.91) in 2020 and −0.51 % (t −1.36) in 2021. Across windows it ranges from −2.51 % (w11, t −2.77) to +2.20 % (w13, t 2.91).
- **F4:** The effect is spread thinly across the coins rather than carried by one. The 2-day excess by coin runs from −0.20 % (BTC, t −0.63) to +0.41 % (XRP, t 0.78), with no coin above t 1. It is weaker in rising markets (−0.26 %, t −0.71, n 416) than in falling (+0.23 %, n 525) or choppy ones (+0.41 %, n 178), but no single profile clears t 2 even among the deepest closes (falling +0.85 %, t 1.88). So no one part of the data carries the effect clearly enough to narrow the idea to.
- **F5:** The test used only the six default coins. The 13 other coins with daily data (ADA, DOGE, LINK, TRX, UNI, AAVE in folds A and D and part of B and C; AVAX, SOL, INJ in A and D; NEAR, SUI, TAO, ONDO in D) were not used. A mean that is the right sign but at t 1.49 needs more independent cases, and those coins supply them on the same 1d bars and folds.

## Ideas
- `069-02.d3.b1_below-high-fade-more-coins` (from F1, F4, F5): When a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next two days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
