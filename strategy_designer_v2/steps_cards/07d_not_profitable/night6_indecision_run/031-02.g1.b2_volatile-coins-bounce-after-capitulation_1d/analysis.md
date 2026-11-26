---
line: 7.d confirmed, not profitable
backtest: 031-02.g1.b2_volatile-coins-bounce-after-capitulation_1d
idea tested: 031-02.g1.b2_volatile-coins-bounce-after-capitulation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6333 USD
---
## Findings
- **F1:** The check failed on Calmar alone (0.7165 against 0.75), and the deepest fall, −7.1 %, is a single day in w14 (2018). That day the book lost 7.04 % while holding the coins lost 9.96 %. Five of the six coins were in a case at once, at allocations up to 1.49, and BTC fell 8.0 %, ETH 12.2 %, LTC 9.7 %, XMR 7.5 % and ZEC 13.3 % the next day.
- **F2:** The cases split by what the 4 days before the deep day did (dropping NaN rows, 314 cases). When those 4 days had already fallen 5–25 %, the next-day excess is +3.30 % (t 3.92, 105 cases). When they were roughly flat, between −5 % and +0.2 %, it is −0.43 % (t −0.87, 104 cases). After a prior rise it is +0.83 % (t 2.09, 105 cases).
- **F3:** Rebuilt at the backtest's cost of 0.19 % per trade, the book changes sharply with the 4 days before the case. Keeping only cases whose 4 prior days fell more than 3 % (132 cases) gives a yearly +4.3 %, a deepest fall of −3.8 % and Calmar 1.11 (Sharpe 0.67). The other 182 cases give Calmar 0.017 and hold the −7.1 % day.
- **F4:** A prior fall alone does not earn, so it is the brief's own "run before the day", not a separate effect. Bars with a 5-day fall below −8 % and no case give −0.15 % next-day excess (t −1.14, 2421 bars), against +1.74 % on the 207 cases where both hold.
- **F5:** A recent capitulation gives the strongest cases. A case with another day at −2 usual moves or worse in the 3 days before has a mean excess of +4.21 % (t 4.22, 40 cases), against +0.88 % without one (t 2.43, 290 cases). Its rebuilt book has a deepest fall of only −1.5 % (Calmar 1.62, yearly +2.4 %).
- **F6:** The recent capitulation alone does not earn: the same bars without a case give −0.39 % next-day excess (t −2.42, 1107 bars).
- **F7:** The vol-target sizing deepens the falls.
- **F8:** The move per case covers the cost: the total is +1.35 %, 7.0 times the 0.19 % cost, and the unusual move is 6.4 times it. The gain is real but uneven across years, near zero in 2018 (+0.01 %, 53 cases) and 2025 (−0.23 %, 34 cases) and large in 2020 (+5.8 %, 29 cases).
- **F9:** The effect is a one-day one. In the top volatility tercile, the mean return over the next 1, 2, 3 and 5 days is +3.19 %, +2.33 %, +1.71 % and −0.51 %, so a longer hold would not help.

## Ideas
- `031-02.g1.b2.d1_capitulation-ending-prior-decline` (from F2, F3, F4, F1): After a day on which a coin falls far more than it usually does in a day and closes near its low, following 4 days in which it had already been falling, it rises over the next 1 day, and the more it fell over those 4 preceding days, the larger that rise.
- `031-02.g1.b2.d2_repeated-capitulation-days-bounce` (from F5, F6, F1): After a day on which a coin falls far more than it usually does in a day and closes near its low, it rises over the next 1 day, and the more such deep down days the coin had in the 3 days before, the larger that rise.
- `031-02.g1.b2.d3_depth-graded-capitulation-bounce` (from F7, F1, F8): After a day on which a coin falls far more than it usually does in a day and closes near its low, it rises over the next 1 day by about the same share of its usual daily move whatever its past 20 days' volatility, and the further the close falls below its usual daily move, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
