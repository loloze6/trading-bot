---
line: 7.b inconclusive
backtest: 031-02.b1.b1_deepest-falls-rebound-most_1d
idea tested: 031-02.b1.b1_deepest-falls-rebound-most
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4042 USD
---
## Findings
- **F1:** The tested rebound is positive but cannot be told from zero, and its mean is carried by a few outliers. Over 30 days the unusual move is +3.60 % with a day-clustered t of 0.99 (145 cases on 97 days). The median case is −2.75 %, only 44.8 % of cases are positive, the 5 %–95 % clipped mean is +0.36 %, and the five best cases add up to 142 % of the total.
- **F2:** Almost all of the positive mean comes from one coin. XRP gives +40.6 % per case (t 1.77, 16 cases). Without XRP the unusual move is −0.98 % (t −0.38, 129 cases on 87 days). The other coins split both ways, for example SOL −14.7 % (t −3.35, 4 cases), BTC −9.1 % (t −1.67), XMR +13.7 % (t 2.47) and DOGE +10.2 % (t 2.23).
- **F3:** The grading the idea depends on is absent.
- **F4:** No other horizon shows the effect more clearly. The unusual move is −0.10 % at 5 days (t −0.13) and −0.11 % at 10 days (t −0.08). It is +1.8 % at 20 days (t 0.83), +3.6 % at 30 days (t 0.99) and +3.5 % at 45 days (t 0.64).
- **F5:** The rebound depends on how much of the fall came in the last 30 days, and that split survives removing XRP.
- **F6:** The same split shows against the 30-day low. Cases sitting at their 30-day low earn −0.3 % (t −0.11, 48 cases). Cases already off the low earn +5.5 % (t 1.31) and +5.6 % (t 0.63).
- **F7:** Years alternate sign, so the effect is mixed rather than small and steady. 2022 gives −12.1 % (t −2.11, 32 cases), 2023 +11.6 % (t 2.34, 35 cases), 2024 +17.8 % (t 1.18) and 2025 −9.1 % (t −2.14, 29 cases).
- **F8:** Cost is not what blocks the idea. The unusual move per case (+3.60 %) is 16 times the 0.22 % cost of a trade, and the total move (+8.76 %) is 39 times. More data would not help much either: the test already used every fold and 15 of the 19 coins, and the four left out exist in fold D only.

## Ideas
- `031-02.b1.b1.b1_steadied-falls-rebound-most` (from F1, F3, F5, F6): While a coin's 90-day return stands below its own usual 90-day move, the higher its 30-day return (the less of the fall came in the last 30 days), the more its price rebounds over the next 30 days. A deep 90-day fall whose last 30 days are still falling hardest keeps falling.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
