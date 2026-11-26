---
line: 7.b inconclusive
backtest: 065-03_falling-agitated-down-streak-rebound_1d
idea tested: 065-03_falling-agitated-down-streak-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3674 USD
---
## Findings
- **F1:** Step 5's main measure, the slope of next-day excess return on the down-streak forecast, was flat at -0.000145 with t -0.36 over 832 days. Yet the bars it is taken on rise clearly on average: +0.49 % unusual move per case, t 2.15, over 768 days. In folds B and C, down days in the profile earn +1.17 % excess (t 2.86, 305 days), while up days in the profile earn -0.96 % (t -2.48). So the rebound is there, but the streak count does not grade it.
- **F2:** The raw count of lower closes is a weak and noisy grade. Mean excess by streak length is +0.74 % (1 day, t 1.58), +1.20 % (2, t 2.76), +1.99 % (3, t 1.47), +1.31 % (4, t 1.10) and +7.19 % (5 or more, t 2.90, only 19 cases). The raw slope is +0.0097 with t 2.16. The plan's forecast standardises the streak over its own past 60 values, which blurs the grade further, and the slope came out at t -0.36.
- **F3:** The depth of the fall over the run of lower closes grades the rebound. Depth here is the log fall over the run divided by the coin's 30-day daily swing. On down days in the profile, the slope of next-day excess on depth is -0.0141 with t -3.11, so deeper falls bring larger rises. The deepest fifth earns +3.03 % (t 2.61). The other four fifths earn +0.08 % to +1.03 %.
- **F4:** Depth carries the effect and the last day's fall does not. With both in one regression, depth keeps a coefficient of -0.0113 (t -2.27). The last day's fall drops to -0.0063 (t -0.63). This is what the brief claims.
- **F5:** The depth effect lives only in the falling, agitated profile. Outside it, the depth slope on down days is -0.0010 (t -0.53). The depth slope points the same way in 5 of the 6 windows with at least 30 cases: w16 -0.020 (t -8.68), w18 -0.021 (t -2.04), w14 -0.008, w15 -0.004 and w9 -0.005. Only w13 is opposite, at +0.004 (t 0.29).
- **F6:** The move is large enough to trade. Per case, the total move is +0.63 %, 2.8 times the 0.22 % cost of a trade. The deepest slides rebound by about +3 % per case, far above that cost.

## Ideas
- `065-03.b1_slide-depth-sets-rebound` (from F1, F3, F4, F5, F6): In a falling, agitated market, when a coin has closed lower on consecutive days, the deeper its total fall over that run of lower closes (measured against its usual daily swing over the past 30 days), the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
