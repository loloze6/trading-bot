---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits above its 200-day simple moving average, the further above it sits, the more the coin rises over the next 20 days compared with its usual 20-day move. This is the tested idea unchanged, on more coins.
Consequence: A trader would know whether distance above the 200-day average deserves a long tilt at all, or whether the faint positive mean here is noise from a few rallies.
Why:
- F1: The forecast's grading only half shows at 20 days. Excess returns over 20 x the coin's mean daily return rise with the forecast: 0-5 gives −0.029 (t −1.63, n 111), 5-10 gives −0.011 (t −0.54, n 100), 10-15 gives +0.002 (t 0.08, n 75) and 15-20 gives +0.055 (t 1.17, n 113). But the Spearman correlation of forecast with excess is only 0.043 (n 399), and it is 0.018 to 0.060 at 5, 10, 40 and 60 days, so no horizon shows a clear effect.
- F4: The effect is small and of mixed sign in every coin. Per-coin 20-day excess on forecast > 0 bars runs from −0.022 (XRP) to +0.059 (ZEC), with every |t| ≤ 0.67, so no coin carries it.
- F2: The positive mean comes from a few large rallies, not from persistence. On forecast > 0 bars the hit rate is below 50% in every forecast bin (0.37 to 0.42 at 20 days), and the median of the allocation-weighted excess is negative for every coin (−0.002 to −0.023) while the means are mostly positive.
