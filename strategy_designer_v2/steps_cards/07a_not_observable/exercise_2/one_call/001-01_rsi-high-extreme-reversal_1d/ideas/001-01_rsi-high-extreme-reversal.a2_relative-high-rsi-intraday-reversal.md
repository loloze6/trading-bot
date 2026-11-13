---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal
line: 7.a not observable
backtest: 001-01_rsi-high-extreme-reversal_1d
instruments: BTC, ETH, BNB
bar: 4h
period: 2021 to 2024
---
Idea: When a coin's RSI(14) on 4-hour bars is high relative to its own previous 60 readings, its return over the next 5 bars is below its average 5-bar return.
Consequence: At the 4-hour scale a trader gets six times as many bars per period, so the reversal after high RSI readings can be traded and checked within a single year.
Why:
- F2: The forecast reached −10 or lower on 15 of 120 bars (12.5%), grouped into 3 episodes, which left only 3 grid cases against the 30 required. At that share, 30 non-overlapping cases would need about 1200 daily bars per coin, roughly 3.3 years.
- F3: The component's logged RSI never exceeded 58.0 (median 47.5, 95th percentile 55.2, 0 bars above 60 or 70), and the bars with forecast ≤ −10 had RSI between 54.0 and 58.0 (mean 55.6). The "high extreme" was therefore only high relative to the 60-bar standardisation, not an absolute extreme. A Wilder RSI(14) recomputed on the closes ranged from 11.9 to 70.1.
- F4: The direction leaned towards reversal but was underpowered. The 3 grid cases had excess 5-bar returns of −13.3%, −0.7% and −6.3% (mean −6.75%, t −1.84). The 15 overlapping extreme bars averaged −2.3% (std 5.7%, t −1.60), and about 23 independent cases would give t = −2 at that effect size, because the 5-bar forward return std is 7.3%.
