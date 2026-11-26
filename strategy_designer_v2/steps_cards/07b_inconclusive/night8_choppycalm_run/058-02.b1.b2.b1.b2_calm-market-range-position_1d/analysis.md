---
line: 7.b inconclusive
backtest: 058-02.b1.b2.b1.b2_calm-market-range-position_1d
idea tested: 058-02.b1.b2.b1.b2_calm-market-range-position
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 1
cost: 0.2331 USD
---
## Findings
- **F1:** The tested idea points the predicted way: the step-5 slope t is +1.70 on 3,436 cases over 506 days, and its size is +0.87 % per case over 5 days (t 3.00, 1,306 days, strength 0.075, 3.9 times the 0.22 % trade cost). In folds B and C alone, the same day-clustered slope at 5 days has t +3.27 (1,056 cases, 236 days). The shortfall therefore comes from folds A and D, and the test already used every coin, fold and day of daily data available, so there is no unused data that could lift it over the bar.
- **F2:** The effect sits in the strongest range positions. Mean 5-day excess return is +3.80 % in the top forecast quintile and −2.55 % in the bottom one. The three middle quintiles show only −0.24 %, −0.22 % and +0.26 %, so a straight-line slope over all bars dilutes it.
- **F3:** Over longer horizons the effect lives in rising and choppy markets, not falling ones. At 10 days the slope t is +3.85 when rising (104 cases), +2.66 when choppy (63) and only +0.51 when falling (125). At 20 days it is +3.03 rising, +1.88 choppy and −0.10 falling. At 5 days all three trends are positive (falling 2.40, choppy 2.83, rising 2.97).
- **F4:** The long side carries more of the effect than the short side at 5 days. The slope t is +2.54 for long cases (547) against +1.74 for short ones (509), with mean excess returns of +1.59 % and −1.28 %.
- **F5:** The effect is not steady across periods or coins in folds B and C:

## Ideas
- `058-02.b1.b2.b1.b2.b1_calm-rising-range-position` (from F3, F1): In a calm, rising market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 10 days.
- `058-02.b1.b2.b1.b2.b2_calm-range-edge-continuation` (from F2, F1): In a calm market, the nearer a coin's close sits to the top of its 20-day high-low range, the larger its rise over the next 5 days, and the nearer to the bottom, the larger its fall, with the move growing faster than the close's distance from the range's middle.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
