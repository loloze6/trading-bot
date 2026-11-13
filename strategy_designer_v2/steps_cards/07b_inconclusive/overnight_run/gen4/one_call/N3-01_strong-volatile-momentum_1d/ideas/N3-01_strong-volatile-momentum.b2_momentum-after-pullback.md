---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.b inconclusive
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin is in a strong, volatile run-up over 20 and 60 days but its close has already fallen back below its 20-day high, it rises more than its usual 5-day return over the next 5 days.
Consequence: A trader would enter a momentum long on a pullback within the run-up, and refuse to buy when the coin is closing at its 20-day high.
Why:
- F4: The effect sits in run-ups that have already pulled back from their 20-day high. Excess is +2.68% (t=1.57, n=107) in the lowest tercile of distance to the 20-day high and +1.60% (t=1.75, n=107, hit 52%) in the middle tercile, against −0.88% (t=−1.01, n=108, hit 43%) for coins at or near their high. The same pattern holds for distance to the 50-bar average: lowest tercile +1.21% (t=1.41, n=76), highest −1.19% (t=−0.77, n=76).
- F1: The pooled effect is a small mean carried by a few large winners: 369 non-overlapping cases at forecast ≥10 give a mean excess 5-bar return of +0.97% (sd 13.5%, t=1.38), but the median is −0.40% and the hit rate is 47%. Skew is 2.43, the top 5% of cases account for 186% of the total excess, and once the tails are winsorised at 5/95% the t falls to 0.97.
