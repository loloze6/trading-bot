---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close stands to its highest close of the previous 90 days, the more it rises over the next 10 days.
Consequence: A trader should lean long for about ten days as a coin's close approaches or passes its 90-day high, and not expect the lift to last to twenty days.
Why:
- F1: At the plan's 20-day horizon there is no effect beyond the reported slope t of 0.73 (827 cases): the rank correlation is -0.014, the slope t is -0.16 once excess returns are clipped at their 2nd and 98th percentiles, and 0.007 once each coin's returns are scaled by their spread.
- F4: The test measured the idea beyond the horizon where it shows: the pooled slope t is 2.27 at 5 days (3,419 cases) and 2.94 at 10 days (1,691 cases), then falls to 0.73 at 20 days, 0.58 at 40 days and -0.23 at 60 days.
- F5: At 10 days the effect holds up better than at 20 days: the slope t is 2.57 on returns scaled per coin and 2.00 with clipped returns, four of six coins are positive (BTC 0.87, ETH 1.53, XRP 1.37, ZEC 3.26), and it is 1.49 without ZEC; the top quintile's excess is +2.5 % (t 2.36) against -0.9 % for the bottom quintile.
- F6: Even at 10 days the effect comes from the closes nearest or beyond the 90-day high: among cases with forecast at or below 2.7 the slope t is 0.16 at 10 days and 0.06 at 5 days, and the top quintile's median is only +0.18 % against its mean of +2.5 %.
- F7: Size is not what blocks the book: at 20 days the total move per case is +3.39 %, 17.6 times the 0.19 % cost of a round trip. Consistent with prior F11, the issue is whether the effect is real, not whether it is large enough to cover costs.
