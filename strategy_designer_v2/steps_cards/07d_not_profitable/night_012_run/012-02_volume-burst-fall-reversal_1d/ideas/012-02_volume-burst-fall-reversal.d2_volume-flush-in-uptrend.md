---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.d not profitable
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 3 days, and the higher the coin's 30-day return before the fall, the larger that rise.
Consequence: A trader would lean hardest into volume-burst falls that hit a coin in a 30-day uptrend, and least into those inside a 30-day decline, where the falls of the book gather.
Why:
- F5: The losses depend on the 30-day trend. Signal bars in the second-lowest 30-day-return quintile (mean −0.128) are followed by a 3-day return of −0.0036, and held bars there lose −0.00065 a bar. The top quintile (30-day return +0.44) gives a 3-day return of +0.0105 and held bars there gain +0.0039; the deepest-fall quintile (−0.32) also rebounds, at +0.0067.
- F6: The deepest falls (largest drawdown −0.238 in w9, Calmar 0.516) gather in falling markets. The worst 5 % of position bars (182, mean −8.1 %) come almost all on the signal day itself. They have a mean 10-day return of −0.068, and 54 % of them have a negative 30-day return, against 43 % of all held bars.
- F4: The rebound sits almost wholly in the strongest forecasts. Signal bars in the top forecast quintile (mean volume ratio 1.89) are followed by a 3-day return of 0.0127. The four lower quintiles give −0.0008 to 0.0042, which is no larger than the coin's own mean.
