---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return, the higher its return over the next 10 days, the more so the lower its 30-day volatility is against its own past.
Consequence: Momentum bets should be held for about ten days rather than twenty, and sized up mainly when the coin is calmer than usual.
Why:
- F1: The effect shows at every horizon shorter than the plan's and weakens at the plan's 20 days. The main measure (forecast/10 × excess return, non-overlapping grid, 6 coins pooled) has t 3.1 at 3 days (5,723 cases), 2.6 at 5 days (3,419), 2.5 at 10 days (1,691) and 2.8 at 15 days (1,115), against 0.57 at 20 days (827) and 0.14 at 40 days (395). The bare sign of the 28-day return follows the same pattern: t 2.4 at 15 days, -0.07 at 20 days.
- F2: Where it shows, the idea's own volatility condition carries the effect. At 5 days the calmest third of 30-day against 90-day volatility gives a main-measure mean of 0.0256 (t 4.2, 564 cases), the most volatile third 0.0014 (t 0.26). At 10 days the calmest third gives 0.042 (t 3.0, 276 cases), the most volatile 0.003 (t 0.27).
- F3: The idea's move covers a trade at 10 to 15 days and not at 20. Per active case the unusual move is 0.63 % at 10 days (strength 0.044, about 3.3 times the 0.19 % round trip) and 1.16 % at 15 days (strength 0.060, about 6 times), against -0.03 % at 20 days. Step 5 measured -0.44 % at 20 days, -2.3 times the cost.
- F5: The effect is graded in the forecast's size and spread over coins and sides.
