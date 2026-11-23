---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday is followed over the next two days, Monday and Tuesday, by a move in the opposite direction, and the larger Sunday's move, the larger the reversal; the effect is strongest when the coin's 30-day volatility is high.
Consequence: A trader would fade Sunday's move into Monday and Tuesday, and lean harder on that bet when the coin has been volatile.
Why:
- F1: Over the two days after Sunday's close, the coins reverse Sunday's own 24-hour move: the slope of the Monday-and-Tuesday excess return on Sunday's volatility-scaled return is -0.0061 (t -3.20, 2173 weekly cases); the mean of the excess return taken against Sunday's sign is +0.82 % (t 5.25) next to a usual 48-hour move of 6.7 %; by quintile, the most negative Sundays are followed by +1.0 % and the second-highest by -1.6 %. Cases on the same weekend are shared across the six coins, so this t overstates how independent they are.
- F2: The reversal grows with the coin's volatility: the slope is +0.0030 (t 1.19) in the lowest volatility tercile, -0.0085 (t -3.02) in the middle one and -0.0137 (t -3.07) in the highest; it is negative for all six coins (t from -0.76 to -2.47) and in 6 of 8 years.
