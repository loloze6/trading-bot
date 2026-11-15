---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A and D
---
Idea: While a coin's 50-day simple moving average stands above its 200-day simple moving average, the coin's return over the next day is higher than its average daily return, and the further the 50-day average stands above the 200-day one, the higher that return.
Consequence: If confirmed on the wider set of coins, golden-cross stretches would be a reason to hold long across many coins, not just the long-lived majors.
Why:
- F1: The test ran on one coin (BTCUSD) and one window (w1, year 2022) of only 120 daily bars, not the 6 windows the plan pooled over. Only 13 bars (10.8 %) had a positive forecast and 107 had none. That is short of the plan's 100 in-stretch bars and gives 1 up-cross stretch against the 3 required.
- F2: The single stretch was already under way at the window's start. It covered bars 0 to 12, all in the first quarter of the window. The 50-day SMA's spread over the 200-day SMA then fell from +50.3 to -56.9 on the standardised scale, averaging -75.0, -83.9 and -63.6 over the later three quarters. The window caught the end of one bull stretch and a bear market, with no new upward cross.
- F4: The outcome is noisy compared with any plausible drift.
