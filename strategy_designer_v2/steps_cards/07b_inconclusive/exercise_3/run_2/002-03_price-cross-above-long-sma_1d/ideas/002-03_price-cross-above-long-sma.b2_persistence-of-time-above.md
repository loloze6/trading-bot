---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's close has stayed above its 200-day simple moving average since crossing it, the larger its rise over the following weeks.
Consequence: A trader would treat a fresh upward cross as no signal and give weight to an above-average state that has lasted.
Why:
- F6: The gain grows with time spent above the SMA. It is +0.0018 within 20 bars of the cross (n 213), +0.0020 at 20–60 bars (n 133) and +0.027 at 60–150 bars (t 0.71, n 53). The plan's "fresh cross" bars carry nothing.
- F1: Bar by bar the effect is close to zero. On the non-overlapping 20-bar grid, bars with forecast > 0 beat the coin's pooled mean by 0.0052 (t 0.32, n 399), against −0.00015 (t −0.01, n 412) for bars below the SMA. Only 40.6% of them win, and the median is −0.036. No horizon from 5 to 60 bars gets past |t| 0.61.
- F3: The effect splits by period. Forecast > 0 bars lost heavily in 2018 (−0.132, t −2.76, n 21) and 2022 (−0.173, t −3.12, n 10). They earned in 2020 (+0.022), 2024 (+0.021) and 2025 (+0.036), and 2020's blocks reached +0.46 (t 2.03). The above-SMA state reverses in bear years and persists in bull years.
