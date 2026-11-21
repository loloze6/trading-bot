---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
line: 7.e profitable but not proven
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return multiplied by its nearness to its 60-day closing high (the closer to the high, the larger the weight), the higher its return over the next 10 days.
Consequence: A trader would size long momentum bets by the plain level of the rise scaled by nearness to the high, rather than by how unusual that level is against its own recent past.
Why:
- F1: The book earns on its long side. Long bars give 10.54 bps per day of the book's 10.47 gross, and short bars give −0.08. By trade, long trades sum to +16,726 % (1,792 trades) and short trades to −1,486 % (1,238). Short trades entered more than 30 % below the 60-day high lose −1,906 % (mean −5.0 %, 33 % winners).
- F4: The book earns where the coin is near its 60-day high, and the 10-day move falls in step with the distance below it. Long contribution is 3.24, 2.84, 2.08, 0.60 and 0.45 bps per day from "at the high" to "more than 30 % below". Over the next 10 days, on the non-overlapping grid, the excess return is +2.08 % (n 122), +1.67 % (194), +0.39 % (399), −0.96 % (376) and −0.70 % (312). Nearness alone has a slope t of 1.63 (n 1,403).
- F5: The test measured a standardised forecast, and that hides the idea. On the 10-day grid, the forecast has a slope t of 1.01 and the recorded component, standardised against its own past 60 values, 1.04. The plain level of the 28-day return times (1/(1+D))² has a slope t of 2.69 (n 1,259), above the 28-day return alone (t 2.29).
- F6: Among coins whose 28-day return is positive, nearness to the 60-day high grades the next 10-day move (t 1.69, n 644). The largest cell is the top quarter of 28-day returns at the high: +4.36 % excess over 10 days (n 79).
