---
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
idea tested: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2494 USD
---
## Findings
- **F1:** The book barely differs from holding the coins. It is in a position on 87–93 % of bars for every coin, with mean allocations from 0.53 (ZEC) to 1.03 (BTC). Its 16 980 trades last 103.5 hours on average, and its daily returns correlate 0.89 with holding's. So it inherits holding's falls (deepest fall −71.4 %, Calmar 0.18) with a Sharpe below holding's (0.50 against 0.55).
- **F2:** The forecast's cases are not the idea's situation. Across its 14 681 cases the unusual 24-hour move is +0.01 % (t 0.21), and the top half by forecast does slightly worse than the bottom half (−0.002 %). The total move per case is +0.15 %, 0.8 times the 0.19 % cost of a trade.
- **F3:** The idea's own situation does carry a move. An hour more than 2 usual moves up on more than 2 times the 30-day volume is followed by an unusual +0.32 % over 24 hours (t 2.96, 3 624 cases), which is +0.46 % in total, about 2.4 times the cost. The same rise on ordinary volume (under 1.2 times) gives −0.05 % (t −0.35, 1 829 cases).
- **F4:** The move grows with the rise times its volume ratio, though not evenly. The lowest quartile of such hours gives +0.15 % (t 0.82) and the highest quartile +0.56 % (t 2.35), 906 cases each.
- **F5:** The continuation is not immediate. After the surging-volume rise the unusual move is −0.04 % at 2 hours and −0.02 % at 6 hours, and it only reaches +0.32 % at 24 hours.
- **F6:** The continuation is strongest when the coin's last 7 days are wild against its 30 days. In the top tercile of 7-day over 30-day hourly volatility the move is +0.66 % (t 2.83), against +0.17 % (t 1.15) in the calm tercile and +0.13 % (t 0.74) in the middle tercile, 1 208 cases each.
- **F7:** A fall on surging volume reverses rather than continues. An hour more than 2 usual moves down on more than 2 times the volume is followed by a rise of 0.38 % above drift over 24 hours (t 3.67 against the fall's direction, 3 932 cases). The rise is 0.35 % (t 2.36) when the coin's 30-day return is positive.

## Ideas
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins.d1_volume-surge-rise-wild-week` (from F1, F3, F4, F6): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's hourly volatility over the past 7 days is high against its past 30 days. The larger that hour's rise times its relative volume, and the higher that 7-day volatility against the 30-day, the larger the further rise.
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins.d2_volume-surge-fall-rebounds` (from F7, F1): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next 24 hours. The larger that hour's fall times its relative volume, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
