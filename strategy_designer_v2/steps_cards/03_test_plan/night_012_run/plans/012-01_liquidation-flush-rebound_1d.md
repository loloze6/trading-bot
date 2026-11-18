---
idea: 012-01_liquidation-flush-rebound
brief: 012_liquidation-flush-partial-rebound
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 70a362722b07
---
Fidelity:
- Situation: a bar closes sharply lower, on volume far above its own 30-day average, with a long lower wick below the close -> kept: a regime rule requires all three on the bar (fall of at least 1 usual move, volume at least 2x the prior 30-day mean, lower wick at least a third of the bar's range).
- Comparison: a more extreme volume burst and a longer wick give a larger rise -> kept: inside the regime the forecast grows with fall x volume ratio and with wick length.
- Outcome: price rises over the next 3 days -> adapted: the position exists only on the flush bar ("after X" made "while X", holding period dropped), and the 3-day rise is measured from the record's closes.
- Verdict transfer: yes: the measure reads the 3-bar rise after the idea's own flush bars and its link to their size, so a confirm or a reject carries over to the idea.
Forecast: The forecast is zero on every bar except a flush bar. A flush bar is one where all three hold: the 1-day return is at most -1 usual move (20-day volatility), volume is at least 2x the mean of the prior 30 days, and the lower wick is at least a third of the bar's range. On a flush bar the forecast is long. It is the equal-weight mean of two standardised parts: (1) the bar's fall in usual moves times its volume over the 30-day mean volume, negated and clipped at 0, and (2) the lower wick as a share of the bar's range. A deeper, heavier fall and a longer wick give a larger long position. The forecast is never negative.
Config: 012-01_liquidation-flush-rebound_1d_config.json
Criterion:
- Horizon: 3 bars
- Main measure: For each flush bar (forecast > 0), take the 3-bar forward return within its window, close[t+3]/close[t] - 1. Subtract the coin's mean 3-bar return over all windows on the non-overlapping grid. Count each flush bar once, dropping a flush bar that falls within 3 bars of an earlier one. Pool all coins and take the t of the mean excess return.
- Supporting check: Across flush bars, the Spearman correlation between forecast and the 3-bar excess return is above 0.
- Confirm: The mean 3-bar excess return is positive with t >= 2 over at least 30 flush cases, and the Spearman correlation is above 0.
- Reject: The mean 3-bar excess return has t <= -2 over at least 30 flush cases.
- Inconclusive: Any t between -2 and 2, or a confirming t with a correlation at or below 0, or fewer than 30 flush cases pooled across coins and windows.
