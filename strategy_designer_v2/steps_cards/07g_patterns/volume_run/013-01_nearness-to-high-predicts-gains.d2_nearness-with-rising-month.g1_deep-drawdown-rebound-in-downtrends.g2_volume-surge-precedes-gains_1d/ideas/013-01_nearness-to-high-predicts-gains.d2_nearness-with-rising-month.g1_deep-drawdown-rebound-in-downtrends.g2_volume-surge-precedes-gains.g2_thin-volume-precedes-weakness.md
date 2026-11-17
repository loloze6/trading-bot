---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The thinner a coin's traded volume over the past day relative to its 20-day average, the lower its return over the next 7 days.
Consequence: Unusually thin trading is a reason to stay out of a coin, or to cut a long, for the following week.
Why:
- F3: In a joint regression, the volatility-scaled one-day return (t 2.07) and the log volume ratio (t 2.12) each carry their own information, but their product does not (t -0.02). Nearness to the 20-day high adds little once both are in (t 1.30, n=2155).
- F4: The volume effect sits at the thin end, not in bursts. In the lowest volume-ratio quintile, the excess 7-day return is -0.0194 (t -3.32, n=432). The other quintiles range from -0.0059 to +0.0089 and none reaches |t| 1.5. The highest quintile is only +0.0035 (t 0.47).
- F5: Thin volume is followed by weakness whichever way the day closed. After thin-volume down days the excess return is -0.0242 (t -2.97, n=201), and after thin-volume up days it is -0.0152 (t -1.83, n=231). After non-thin up days it is +0.0107 (t 2.32, n=915).
