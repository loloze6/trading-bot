---
line: 7.b inconclusive
backtest: 067-01.b1.g1.b1.d1.g3_chop-slide-twenty-day-continuation_1d
idea tested: 067-01.b1.g1.b1.d1.g3_chop-slide-twenty-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3942 USD
---
## Findings
- **F1:** The fall-side continuation is concentrated in the first days and fades by step 5's horizon. On non-overlapping grids inside the choppy profile, after a negative 30-day return, the mean unusual move in the short's direction is +2.84 % over 5 days (t 2.19, cases of one day together; 204 cases on 105 days). It is +2.76 % over 7 days (t 1.56), +3.36 % over 10 days (t 1.33), -0.23 % over 14 days (t -0.05) and +1.76 % over 20 days (t 0.40, 49 cases on 26 days). The 20-day figure matches step 5's +0.75 % with t 0.45: the test measured the idea at a horizon where it no longer shows.
- **F2:** Over 5 days the continuation grows with the depth of the slide. Split into thirds by the 30-day return, the deepest third (mean 30-day return -28.9 %) gives +4.40 % (t 1.70), the middle third (-13.5 %) gives +3.38 % (t 2.12) and the shallowest third (-3.3 %) gives +0.75 % (t 0.65). Slides deeper than 10 % give +3.80 % (t 1.94, 121 cases), against +1.44 % (t 1.37, 83 cases) for shallower ones.
- **F3:** Over 20 days the effect is drowned by the market's own moves. The fall-side continuation swings from window to window: +19.1 % in w7, -18.6 % in w8, +14.9 % in w9, -14.2 % in w10, -37.6 % in w11, -27.4 % in w17 and +26.8 % in w18. The coin's usual 20-day move is 25.96 %, against an unusual move of 0.75 % per case (strength 0.009).
- **F4:** The 5-day continuation is positive in every period group: +0.97 % in w7–w10 (70 cases), +2.77 % in w11–w14 (71 cases) and +5.01 % in w15–w18 (63 cases). The 10-day continuation is already -0.19 % in w7–w10.
- **F5:** The rise side does not continue in this data, so the shown effect is the fall side the tested idea names. After a positive 30-day return, the unusual move in the rise's direction is +4.17 % over 5 days (t 0.99, 96 cases), -0.36 % over 20 days (t -0.13, 89 cases) and -5.78 % over 40 days (t -1.24).
- **F6:** At 5 days the move covers the cost of a trade. The unusual move of +2.84 % per case is about 13 times the 0.22 % cost of a trade, and the total move in the short's direction is +1.62 %. At 20 days the total move is -2.45 %, because the coins' normal drift of -3.20 % works against the short.

## Ideas
- `067-01.b1.g1.b1.d1.g3.b1_chop-slide-five-day-continuation` (from F1, F2, F3, F4, F6): In a choppy market, the larger a coin's percentage fall over the past 30 days, the more it keeps falling over the next 5 days, the continuation growing with the depth of the slide.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
