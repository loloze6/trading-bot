---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is a fall, the higher its close has climbed back inside its 30-day high-low range, the further it falls over the next 5 days.
Consequence: A trader would treat a rebound into the upper part of the range after a 30-day fall as a chance to sell, not as a turn.
Why:
- F4: Outside the trending regime, a coin whose 30-day return is negative but whose close has climbed back above the middle of its range falls hardest. Its 5-day unusual move is −2.05 % (t −4.17, 399 cases). Below the middle after a fall it is −1.07 % (t −3.50, 1194 cases), and above the middle after a rise it is +0.93 % (t 2.48, 933 cases).
- F2: Contrary to the brief, the coin's place in its 30-day high-low range predicts continuation, not a return to the middle. In the bars outside the trending regime, the 5-day unusual move rises with the close's position in the range: slope +0.0253 (t 2.88, n 3097), from −1.08 % in the lowest fifth (t −2.60) to +0.11 % in the highest. Over 10 days the slope is +0.0657 (t 3.66, n 1548).
