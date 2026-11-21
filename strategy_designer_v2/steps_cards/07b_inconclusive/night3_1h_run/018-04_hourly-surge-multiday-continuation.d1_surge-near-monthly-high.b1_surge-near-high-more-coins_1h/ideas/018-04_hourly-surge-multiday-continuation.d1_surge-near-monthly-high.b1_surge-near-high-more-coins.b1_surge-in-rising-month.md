---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high.b1_surge-near-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while the coin's 30-day return is positive: the larger the surge and the closer the close to its 30-day high at that hour, the larger the rise.
Consequence: A trader would buy hourly surges only in coins that are up over the past month, and refuse the same surges in coins down over the month, which on average fall further.
Why:
- F1: The tested result is on the predicted side but short of the bar, and no more hourly data exists to raise it. Across 4,984 cases the mean unusual 120-hour move is +0.35 % (t 1.83), a strength of 0.028. Only 46 % of cases are positive, with a median of −0.86 %. The test already used all 19 coins and all four folds, and the hourly bars end in 2025.
- F2: The effect splits cleanly on the sign of the coin's own 30-day return at the signal hour (3,669 cases have one).
- F3: The split runs across the full range of the 30-day return, not just at its sign.
- F4: Inside the positive 30-day return cases, the move is still graded by the forecast. The upper half of the forecast averages +1.87 % (t 3.01) against +0.95 % (t 2.30) for the lower half, 846 cases each.
- F5: The positive 30-day return effect is broad across coins but not across years.
- F7: Nearness to the 30-day high, the tested condition, does not grade the move monotonically.
