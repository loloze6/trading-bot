---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.b inconclusive
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes up by an outsized amount (about 2σ of its recent daily moves) while its close is already well above where it was 20 days earlier, it keeps rising over the next five days, beginning from the day after the shock.
Consequence: A trader would take a long after a shock-up day only when the coin is already in a 20-day uptrend, and refuse the same shock in flat or falling coins.
Why:
- F4: The effect sits in coins that were already rising. Events in the top tercile of the prior 20-day return gain +2.97% over 5 bars (t 2.35, n 163). The low and mid terciles gain +0.08% (t 0.11) and −0.35% (t −0.49).
- F5: Measured from the bar after the event (bars t+1 to t+5), top-tercile prior-20-day events gain +2.68% (t 2.61, n 163, hit 58.9%). The next-bar excess over all events is −0.20% (t −0.88), so any continuation starts after the first day.
- F1: The 601 independent big-up-day events have a mean 5-bar excess return of +0.88% (t 1.67), but the median is −0.22%, the hit rate is 48.9%, the skew is 2.4 and the 5%-trimmed mean is only +0.34%, so a few large winners lift the mean while the typical event goes nowhere.
- F3: The effect changes sign across years. Events gain in 2021 (+2.97%, t 2.08, n 74) and 2024 (+3.35%, t 2.72, n 77) and lose in 2022 (−4.60%, t −2.82, n 67) and 2018 (−0.49%, hit 34%, n 62), so a pooled t near 1.7 averages opposing regimes.
