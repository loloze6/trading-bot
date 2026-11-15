---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the wider the percent spread between the two, the more the coin rises over the next 10 days relative to its usual 10-day return.
Consequence: If confirmed on the wider coin set, a long position sized by the golden-cross spread is justified; if rejected, the spread is no reason to buy.
Why:
- F1: The tested slope is near zero at every horizon, not only the plan's: 0.000202 with t 0.37 at 10 days (1657 non-overlapping blocks, 832 with forecast > 0); t 0.20 at 5 days (3349 blocks), 0.55 at 20 days (811) and 0.09 at 30 days (529); on forecast > 0 blocks alone the slope is t 0.37 (832).
- F3: The result is mixed across coins. The per-coin t runs from -0.28 (XRP) to 0.94 (BTC), and the mean excess return on forecast > 0 blocks is positive for ETH (0.0063), ZEC (0.0073) and BTC (0.0024) but negative for LTC (-0.0086), XRP (-0.0046) and XMR (-0.0011).
