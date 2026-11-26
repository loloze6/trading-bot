---
line: 7.b inconclusive
backtest: 032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise_1d
idea tested: 032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1946 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: the mean timing gain is +0.00324 with t 1.43 on 1691 grid cases over 304 days, the supporting check passes (+2.01 % for forecast ≥ +2 minus forecast ≤ −2), and the idea's size is +1.31 % unusual move per case (t 2.13, 688 days, strength 0.086).
- **F2:** The effect is spread across the coins rather than carried by one: on folds B and C the 10-day timing gain is positive for all 6 coins (BTC +0.0010 t 0.27, ETH +0.0056 t 1.13, LTC +0.0027 t 0.55, XMR +0.0035 t 0.78, XRP +0.0160 t 2.05, ZEC +0.0068 t 1.33, 141 cases each), but no coin except XRP is clear alone.
- **F3:** The effect is also spread across time but is noisy within it: 9 of 12 windows have a positive gain, but only w16 is clear alone (+0.0364, t 2.64). By year, 2018 is −0.0039 (t −0.48), 2019 is +0.0014, 2020 is +0.0169 (t 2.33) and 2021 is +0.0090, so each period holds too few independent 10-day cases (11 to 20 days per window) to show it.
- **F4:** The effect is graded at the extremes and flat in the middle: excess 10-day returns are +3.79 % for forecasts above +4 (132 cases) and −3.01 % for forecasts at or below −4 (192 cases), while the four middle buckets lie between −0.92 % and +0.93 %.
- **F5:** The effect holds on both sides and in both 28-day return states: long cells have a mean excess of +0.98 % (466 cases) and short cells −1.20 % (380 cases). The timing gain is +0.0080 (t 1.52) when the 28-day return is negative and +0.0047 (t 0.97) when it is positive, as the idea's "whatever its 28-day return" says.
- **F6:** The horizon is not the cause of the unclear result: on folds B and C the gain is +0.0044 (t 2.18, 1710 cases) over 5 days, +0.0059 (t 1.55, 846 cases) over 10 days and −0.0028 (t −0.38, 414 cases) over 20 days. The 10-day test sits near the effect's horizon and is limited by its number of independent days.
- **F7:** More data is available than the test used. It ran only the 6 default coins, while folds A and D also hold ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL and INJ, fold D holds NEAR, SUI, TAO and ONDO, and folds B and C hold part of ADA, DOGE, LINK, TRX, UNI and AAVE.

## Ideas
- `032-02.g1.e1.e1.e1.b1_unusual-nearness-more-coins` (from F1, F2, F3, F5, F7): The closer a coin closes to its highest close of the last 28 days, compared with how close it has usually closed over the past 60 days, the larger its rise over the next 10 days, whatever its 28-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
