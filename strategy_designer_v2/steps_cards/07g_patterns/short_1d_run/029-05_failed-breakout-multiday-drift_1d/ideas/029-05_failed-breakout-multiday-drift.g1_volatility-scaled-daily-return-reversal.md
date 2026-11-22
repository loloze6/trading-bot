---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's daily rise in units of its 20-day volatility, the larger its fall over the next 8 days, and the larger its daily fall in those units, the larger its rise over the next 8 days.
Consequence: Shorting a coin is better done after its outsized up days than after breakdowns, and a short taken right after a sharp down day should be refused.
Why:
- F1: Over 8 days a coin moves against its last daily return, scaled by its 20-day volatility. Regressed on that scaled return, the 8-day unusual move has a slope of -0.0165 with t -4.57 over 1691 independent cases. The lowest quintile is followed by +2.87 % (t 3.20) and the fourth quintile by -2.30 % (t -3.64).
- F2: This reversal holds in every coin and in both halves of the windows. Top-minus-bottom quintile differences run from -1.9 % (LTC) to -9.0 % (ZEC), with Spearman rho from -0.087 to -0.188. In w1-12 the extreme quintiles have t +3.36 and -3.95; in w13-24, +1.40 and -1.80.
- F7: The book's short exposure does not follow the reversal. The share of bars held short stays between 25 % and 30 % in every quintile of the scaled daily return, so the shorts come no more after up days than after down days.
