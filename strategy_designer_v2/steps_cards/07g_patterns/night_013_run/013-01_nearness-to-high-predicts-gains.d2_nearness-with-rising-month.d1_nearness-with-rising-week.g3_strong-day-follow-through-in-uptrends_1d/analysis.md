---
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3564 USD
---
## Findings
- **F1:** The book's loss comes from its short side. Short bars summed a position gain of -6.64 over 4141 bars, against +6.40 over 5062 long bars, and the short side lost on every one of the six coins (from -0.40 on BTC to -2.08 on XMR). Of the short side's -6.64, -4.68 is timing and -1.95 is drift.
- **F2:** Over one day the forecast's strongest bearish readings are followed by a rebound, not a fall. Bars with forecast at or below -10 (a large down day inside an up-month) were followed by a mean next-day return of +0.60% over 1252 bars. Mid-range and flat forecasts were followed by about +0.06%, and the bullish forecasts of 5 to 10 by -0.09%. This bounce is what makes the shorts lose even though the 7-day slope confirms.
- **F3:** Over 7 days the forecast does sort returns at both ends within trending bars. The bottom quintile's excess return was -1.93% (t -2.22, n 245) and the top quintile's was +2.71% (t 2.34, n 243), with the middle quintiles flat. So the 7-day edge and the 1-day rebound in F2 point opposite ways on down days.
- **F4:** Rising recent volume predicts higher 7-day returns, the strongest pattern seen across all angles. The log of the 7-day mean volume over the 30-day mean volume has a slope of 0.028 on the 7-day excess return (t 3.47, n 1723 non-overlapping cases), t 2.73 in trending bars and t 3.34 in the later windows. It is carried mostly by XRP (t 3.09) and ZEC (t 2.58).
- **F5:** Closeness to the 30-day high helps mainly when volume is also rising. Coins in the top tercile of closeness and the top tercile of 7-day volume earned +2.17% excess over 7 days (n 250), against +0.11% for the top closeness tercile with low volume (n 129) and about -1.2% for the bottom closeness tercile. This runs against the brief's worry that follow-through comes on thin volume.
- **F6:** Closeness to the 30-day high scaled by 30-day daily volatility predicts the 7-day excess return (slope 0.0040, t 3.10, n 1723; t 2.17 in trending bars). Raw closeness is weaker (t 1.51).
- **F7:** Not counted as findings: the Friday excess of +3.57% appears only in the early windows. The negative slope of the 30-day return in falling months (t -2.35) is borderline given the number of angles examined.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends` (from F1, F2): While a coin's 30-day return is positive, the larger its latest one-day fall relative to its 30-day daily volatility, the higher its return over the next 1 day.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g2_building-volume-predicts-gains` (from F4, F5): The higher a coin's 7-day average volume relative to its 30-day average volume, the higher its return over the next 7 days.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g3_volume-backed-nearness-to-high` (from F5, F6): The closer a coin's close is to its 30-day high, measured in units of its 30-day daily volatility, the higher its return over the next 7 days, and the more so the higher its 7-day volume relative to its 30-day volume.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
