---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 20-day volatility is low compared with its own past levels, the larger its one-day move relative to its usual daily move, the further it moves the same way over the next day.
Consequence: A trader would refuse to fade a sharp one-day move in a calm market and would instead lean with it for the following day.
Why:
- F7: On low-volatility days, moves continue the next day instead. The pooled slope is positive (t +2.70), and it is positive for BTC (t 2.26), ETH (t 2.05), ZEC (t 1.84), XRP (t 0.61) and LTC (t 0.33); XMR is the exception at t -0.21. The per-coin values are weak on their own.
- F3: The book's own gain follows the volatility split. Position × next-day return averages +0.00231 per bar in the high-volatility tercile (t 7.15, n 5315) and -0.000868 in the low-volatility tercile (t -2.19, n 5315). The book's overall loss therefore comes from fading moves on calm days.
