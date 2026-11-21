---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, only while its 20-day daily volatility is high against its own past year, and the more so the higher that volatility stands.
Consequence: A trader should buy a coin's vol-scaled down day for one day only in its turbulent, high-volatility stretches, where the rebound is several times a round trip, and refuse the same trade in calm stretches.
Why:
- F2: The effect is not convex, so the supporting check failed. The middle forecasts 5 to 20 earned +0.39 % (t 1.90, 436 cases), the forecasts at the cap of 20 only +0.06 % (t 0.24, 344). On raw size, falls of 2 to 3 of the 20-day volatility earned +0.96 % (t 2.08, 113), and falls beyond 3 earned −0.29 % (t −0.19, 28).
- F3: The rebound sits in high-volatility periods. Among forecast ≥ 5 bars, the highest third of 20-day volatility earned +1.15 % excess the next day (t 2.90, 219 cases), against −0.22 % (t −1.04) in the lowest third and −0.02 % (t −0.07) in the middle third.
- F4: The effect is too small for its cost overall. The unusual move is +0.06 % per case, 0.014 of the 4.01 % usual daily move, which is 0.5 times the 0.11 % round trip (about 10–11 bps on BTC and ETH by topic 38). The high-volatility third's +1.15 % is about 10 times that cost.
- F6: Across all down days, the size of the fall barely ranks the next day's return (correlation 0.025, 2,389 days). The idea's grading by fall size alone is weak; the grading shows only through the volatility state.
