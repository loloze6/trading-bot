---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the last hour, measured against its 1-day volatility, the larger its rise over the next 1 hour.
Consequence: A trader would buy into a sharp hourly drop for the following hour, sized to how sharp the drop was, and refuse the trade if the rebound proves absent.
Why:
- F3: The next hour's excess return falls steadily across deciles of the last hour's return scaled by 1-day volatility. It runs from +4.6 bp (t = 7.1, n = 41,310) after the sharpest falls to −3.2 bp (t = −6.5) in decile 9 and −1.6 bp (t = −2.6) in decile 10. This t is not clustered by day, so it is likely overstated. The rebound after sharp falls is positive in all 6 coins and largest in the smaller coins (ZEC +9.1 bp, XRP +6.1 bp, BTC +2.8 bp). Over the next 6 hours, the lowest quintile keeps only +4.6 bp (t = 2.0), so most of the effect is in the first hour.
