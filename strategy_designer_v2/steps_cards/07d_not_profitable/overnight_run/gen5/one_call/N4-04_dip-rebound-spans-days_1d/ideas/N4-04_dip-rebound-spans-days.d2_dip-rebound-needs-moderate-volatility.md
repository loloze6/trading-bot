---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-04_dip-rebound-spans-days
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In an uptrending coin, a sharp one-day drop is followed by a rise over the next three days when the coin's recent daily volatility is moderate. When recent volatility is in its highest third, the drop is followed by a larger spread of outcomes around a flat mean.
Consequence: A trader refuses dip entries when the coin's 20-day realised volatility is in its top tercile, which removes the deepest drawdown days.
Why:
- F4: The rebound disappears in the most volatile state. By coin-wise 20-day volatility tercile, the forward 3-bar return is +0.83% (t 2.11, n=358) when calm, +2.05% (t 4.18, n=357) in the middle and +0.49% (t 0.81, n=361) when wild, with days 2–3 at −0.03% (t −0.06). The wild tercile's active book days have a standard deviation of 9.0% and a worst day of −33.5%.
- F1: The book fails on Calmar (0.54 against the 0.75 needed) because its gain and its drawdowns both sit in the fully sized days: days with a position of 1.5–3 (n=703) earn a mean of +1.58% but with a standard deviation of 11.0% and a worst day of −37.6%, while days at ≤0.5 (n=1144) earn +0.01%. Window drawdowns grow from about −5% to −10% in w1–w10 to −12% to −27% in w11–w24 (worst −51% in w12).
