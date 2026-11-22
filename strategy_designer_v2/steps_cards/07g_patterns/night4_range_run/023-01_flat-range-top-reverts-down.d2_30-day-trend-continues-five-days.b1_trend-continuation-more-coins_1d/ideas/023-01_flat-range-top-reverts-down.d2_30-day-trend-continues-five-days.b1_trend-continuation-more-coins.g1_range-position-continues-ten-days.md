---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's close sits inside its own 30-day high-low range, the higher its return over the next 10 days, and the lower it sits, the further it falls.
Consequence: A trader would buy coins near the top of their 30-day range and refuse to buy dips near its bottom, rather than fade the range edges.
Why:
- F2: Contrary to the brief, the coin's place in its 30-day high-low range predicts continuation, not a return to the middle. In the bars outside the trending regime, the 5-day unusual move rises with the close's position in the range: slope +0.0253 (t 2.88, n 3097), from −1.08 % in the lowest fifth (t −2.60) to +0.11 % in the highest. Over 10 days the slope is +0.0657 (t 3.66, n 1548).
- F3: The same continuation from the range position holds on all bars together. The slope is +0.0245 over 5 days (t 3.87, n 5434) and +0.0523 over 10 days (t 4.23, n 2680). It is still there inside the trending regime (slope +0.0209, t 2.21, n 2337), so a regime rule does not create it.
- F6: The range-position continuation outside the trending regime fades over time. In the range position's direction it is +1.37 % to +2.67 % a year in 2018–2021 (t up to 3.88) and between −0.17 % and +0.30 % in 2022–2025 (all |t| < 0.6).
