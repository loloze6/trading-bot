---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 3 days above its usual drift, only while the coin's 30-day return is positive.
Consequence: A trader would lean long after unusually wide days in coins that are up over the past month, more strongly the wider the day, and stay out of the market otherwise, which cuts both the downtrend falls and the idle low-forecast days.
Why:
- F2: The effect lives only while the coin's 30-day return is positive: there the pooled slope of 3-day excess on the forecast is 0.00284 (t 3.96, n 2187), and when it is negative it is -0.00047 (t -0.63, n 2096); the 3-day excess rises in steps in rising markets (-0.27 %, -0.05 %, -0.27 %, +0.56 %, +2.03 % with t 3.71 at the widest, n 345).
- F3: A rising 30-day return is not an effect of its own: in rising markets, grid cases without a wide day had 3-day excess of -0.19 % (n 1585), against +1.40 % (t 3.79, n 602) when the day was also wider than its norm; in falling markets wide days gave -0.31 % (n 670). The trend belongs to the idea's own theory, because range expansion that follows a trend is trend-following traders adding, not panic.
- F4: The book's deepest falls came in falling windows: w9 fell -12.9 % while its coins fell 32 %, and w2 fell -9.2 % while its coins fell 44 %, with long positions losing -0.25 in w2. Being long on wide days inside a downtrend is what feeds the Calmar failure (0.42).
- F5: The book was in a position on 99 % of coin-days, mostly with small positions near a zero forecast (mean |allocation| 0.09–0.11 for |f| < 1.5, 14 % of bars with |f| < 0.5). That is why the mean on days in a position is 0.016 % against the required 0.05 %, while the bars with f > 3 carried +2.34 of the +3.6 summed gain.
- F6: The move is large against the cost where the effect holds: wide days in rising markets were followed by a total 3-day move of +1.77 % (9 times the 0.19 % trade cost) and a 6-day move of +3.28 % (excess +2.54 %, t 2.93, n 310), while the 10-day move fades (t 1.46).
