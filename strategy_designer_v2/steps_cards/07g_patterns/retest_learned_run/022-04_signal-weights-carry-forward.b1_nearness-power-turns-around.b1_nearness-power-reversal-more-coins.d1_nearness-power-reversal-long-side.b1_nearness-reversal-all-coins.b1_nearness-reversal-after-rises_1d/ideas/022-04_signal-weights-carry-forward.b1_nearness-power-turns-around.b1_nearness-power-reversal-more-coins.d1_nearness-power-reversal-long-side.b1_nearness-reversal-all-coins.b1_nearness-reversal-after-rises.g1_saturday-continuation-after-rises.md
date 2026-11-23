---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: On Saturdays, the higher a coin's 5-day return to Friday's close relative to its 30-day volatility, the higher its return over the next 1 day.
Consequence: A trader should go long a coin into Saturday in proportion to how strongly it rose over the past 5 days, and refuse that long when it fell over those days.
Why:
- F1: Saturday is the one weekday that stands out across coins. The day-by-day cross-coin mean on Saturdays is +0.500 % (t 3.28, 414 days), against +0.045 % on the other days (Welch t 2.60, 414 against 2,484 days). It is positive in 15 of the 16 coins with Saturday data, INJ being the exception, and positive in every year 2018–2025 (from +0.11 % to +0.78 %). Its daily standard deviation is also lower, 3.91 % against 4.94 %.
- F2: Saturday's return is graded by the coin's 5-day return up to Friday's close, scaled by its 30-day volatility. By quartile, from bottom to top, it is −0.24 %, +0.12 %, +0.76 % and +1.10 % (rank slope t 3.46, clustered by day, 2,677 coin-days). The grading is weaker for the previous single day (slope t 1.94) and for the 30-day return (slope t 1.81).
- F3: Saturday's return is not graded by volatility. By 30-day volatility quartile it is +0.37 %, +0.41 %, +0.36 % and +0.57 % (slope t 0.55). Relative to the coin's usual volatility the slope is −0.72, so the Saturday gain is not a high-volatility artefact.
