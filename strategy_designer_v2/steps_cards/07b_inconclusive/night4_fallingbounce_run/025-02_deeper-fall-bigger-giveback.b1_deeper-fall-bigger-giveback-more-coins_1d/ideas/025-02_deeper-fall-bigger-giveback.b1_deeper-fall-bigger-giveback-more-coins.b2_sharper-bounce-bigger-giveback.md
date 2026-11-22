---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins
line: 7.b inconclusive
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, the larger its one-day rise measured in its usual daily moves, the larger its fall over the next day.
Consequence: In a falling coin, a trader would fade the sharpest one-day rises hardest, expecting the largest part of the bounce to be given back the next day.
Why:
- F4: Across all 445 cases, the size of the bounce day itself grades the next day's move. The slope of the excess 1-day return on the bounce day's return is -0.148 (t -3.92, 441 cases) and still -0.222 at 5 days (t -2.29). The top bounce quartile gives back -2.10 % the next day (t -3.11, 92 cases). The grading is not monotone, because the smallest quartile also falls (-0.75 %, t -1.44).
- F1: The tested grading does not hold, and points the wrong way at longer horizons. Across the 445 bounce cases in a falling 90-day market (one per 5-day grid cell), the slope of the excess return on the 90-day return has t -1.23 at 5 days and t -2.08 at 10 days. By quartile, the deepest 90-day falls are followed by a rise: +1.36 % excess over 5 days (t 1.05, 112 cases) and +3.87 % over 10 days (t 2.13). The second quartile falls -3.69 % over 10 days (t -2.74). This is why step 5's slope t was -0.47 and its supporting mean was -0.10 % per case.
- F6: The tested idea's measured size is too small to pay, while the next-day giveback of F2 is large enough. The unusual move per case is -0.10 % over 5 days, -0.4 times the 0.22 % cost of a trade. The next-day giveback where the 30-day return is negative is about 8 times that cost.
