---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly.g1_volatile-fall-next-day-rebound_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 20-day volatility is high relative to its last 100 days, the higher the day closes within its own high-low range, the lower its return over the next day, and the lower it closes, the higher that return.
Consequence: In volatile stretches a trader can lean against where the day closed in its range, buying weak closes and fading strong ones for one day.
Why:
- F1: When the 20-day volatility is above its 100-day mean, the next day's excess return falls steadily with where the day closed within its range: closes in the bottom fifth average +0.0058 (t 2.04, n 333) and closes in the top fifth average −0.0046 (t −2.32, n 560), a low-minus-high Welch difference of 0.0117 (t 3.23); outside that regime the same split shows nothing (−0.0019 vs +0.0004).
- F2: Inside the high-volatility regime, the close's place in the range carries the effect within each side of the day: down days closing in the lower third gain +0.0050 next day (t 2.46, n 527), and up days closing in the upper third lose −0.0046 (t −2.87, n 696); but in a joint regression with the day's sized move, the close-location slope is not separate (t −1.05) while the move's slope is (t −2.07).
