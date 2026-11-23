---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over Monday and Tuesday a coin moves in the direction of its Saturday 24-hour return minus its Sunday 24-hour return, and the larger that difference, the larger the move.
Consequence: A trader would follow Saturday's move only after setting Sunday's move against it, and would refuse the trade when Sunday has already carried Saturday's move further.
Why:
- F3: In the same regression, Saturday's continuation and Sunday's reversal each stand on their own: Saturday's return has beta +0.0104 (t 5.03) and Sunday's -0.0051 (t -2.68). The combined weekend 2-day return predicts nothing monotone (quintiles +0.28 %, -0.85 %, -0.47 %, +0.02 %, +0.30 %), because the two days pull opposite ways.
- F4: Saturday's move continues only once the week starts: read at Saturday's close, its slope over Sunday and Monday is +0.0011 (t 0.61); read at Sunday's close, its slope over Monday and Tuesday is +0.0110 (t 5.34). The book earns its money on those days: 22.1 bp per coin-day on Mondays and 12.0 bp on Tuesdays, against -2.4 to +1.2 bp on the other days.
- F1: Over the two days after Sunday's close, the coins reverse Sunday's own 24-hour move: the slope of the Monday-and-Tuesday excess return on Sunday's volatility-scaled return is -0.0061 (t -3.20, 2173 weekly cases); the mean of the excess return taken against Sunday's sign is +0.82 % (t 5.25) next to a usual 48-hour move of 6.7 %; by quintile, the most negative Sundays are followed by +1.0 % and the second-highest by -1.6 %. Cases on the same weekend are shared across the six coins, so this t overstates how independent they are.
