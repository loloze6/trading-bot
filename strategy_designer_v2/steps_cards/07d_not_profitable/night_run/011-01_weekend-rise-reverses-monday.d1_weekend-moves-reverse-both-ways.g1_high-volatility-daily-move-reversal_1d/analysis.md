---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3358 USD
---
## Findings
- **F1:** The gain is carried by the long side alone. Active bars held long earned a gross 0.002538 per bar over 3922 cases, against 0.000073 over 4196 short bars. So fading up days adds almost nothing while it keeps the book out of the coins' rise: the book's mean daily return was 0.000286 against holding's 0.001180, and its Sharpe 0.516 against holding's 0.554.
- **F2:** Up days do not reverse in a way that pays. After the largest third of vol-scaled up days the next-day return minus the coin's mean was only -0.000260, and the net gain was -0.002066 per bar over 1194 cases. After large down days the next day beat the coin mean by 0.008049, with a net gain of 0.005421 over 1075 cases.
- **F3:** Fees take about half the gross. Active bars earned 0.001260 gross against 0.000605 in fees. Small and mid moves net almost nothing: down-small 0.000005, down-mid 0.000341, up-small -0.000418, up-mid 0.000083.
- **F4:** Inside the active regime the gain grows with how far 20-day volatility stands above its 120-day median. In the top quartile of that ratio (1.67 to 7.19) bars earned 0.003502 gross and 0.002927 net. The two middle-low quartiles (0.45 to 1.29) earned 0.000349 and -0.000671 gross, and -0.000175 and -0.001380 net, about 1044 bars each.
- **F5:** The book's falls do not come from the market falling. Its deepest chained fall was -0.325 (Calmar 0.27). On its worst 5% of days (145 days, book -0.0258) the coins' mean return was -0.000079, and the coins rose on 60% of those days, which matches the short side being run over on up days.

## Ideas
- `011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.d1_high-volatility-down-day-rebound` (from F1, F2, F4, F5): When a coin's 20-day volatility is high relative to its own 120-day volatility, its last day's move reverses over the next 1 day, but only for down days: the larger that day's fall measured in its 20-day volatility, and the higher its 20-day volatility stands against its 120-day volatility, the larger the rise over the next 1 day.
- `011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.d2_large-falls-rebound-next-day` (from F2, F3): A coin's rise over the next 1 day after a down day grows with the size of that day's fall measured in its 20-day volatility, and it is concentrated in the largest falls, where it is several times larger than after small falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
