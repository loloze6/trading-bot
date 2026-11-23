---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3568 USD
---
## Findings
- **F1:** In coins whose 30-day return is negative, wide days (range above the 30-day mean range) that close in the top third of their range are followed by a 3-day excess return of −3.59 % (t −4.22, 69 non-overlapping cases) when the day is in the widest third. The same cases give −1.29 % (t −1.37, 67) in the middle third and −0.17 % (t −0.19, 69) in the narrowest third, so the fall grows with the width.
- **F2:** On down-30-day wide days, a combined score (range excess over the norm × close location from −1 at the low to +1 at the high) ranks the next 3 days' excess return. The Spearman rho is −0.110 (p 0.006, 615 cases), and the top score quintile averages −2.26 % (t −3.26, 123 cases) while the other four quintiles lie between −0.20 % and +0.37 %.
- **F3:** The down-trend wide high-close fall is not one coin or one year. Four of six coins are negative (BTC −2.28 % t −1.93, ETH −4.20 % t −3.71, LTC −2.90 % t −2.37, XMR −2.11 % t −2.37; XRP +0.58 %, ZEC +1.45 % not significant). Four of eight years are below −2 % with |t| ≥ 2.8 (2019, 2020, 2022, 2025). 66 % of the 101 coin-windows are negative.
- **F4:** The down-trend wide high-close move is large next to a usual move: its mean strength is −0.24 of the coin's usual 3-day move, against 0.053 for the tested idea. It shows already on the next day, with a mean 1-day excess of −1.48 %.
- **F5:** The mirror case does not reverse. In up-30-day coins, wide days that close in the top close-location quintile are followed by +1.54 % (t 2.51, 205 cases), and every close-location quintile is positive (+0.15 % to +1.54 %). The sign of what follows a wide high-closing day therefore depends on the 30-day trend.
- **F6:** The tested idea's effect sits almost entirely in the widest-range quintile of up-trend bars: +1.53 % (t 3.78, 567 cases). Quintiles q2 to q4 are negative (−0.62 %, −0.28 %, −0.18 %), and down-trend bars show no width effect (rho −0.020, p 0.36, 2096 cases).
- **F7:** Across weekdays, 1-day return quintiles, volatility terciles and 30-day return quintiles, no other group passed |t| 2 except the second 30-day return quintile (−0.50 %, t −1.99, 856 cases). Among about 40 groups looked at, that one is consistent with chance.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise.g1_downtrend-wide-day-rallies-fade` (from F1, F2, F3, F4, F5): In a coin whose 30-day return is negative, a day whose high-low range is wide against its 30-day average range and whose close sits near the day's high is followed by a fall over the next 3 days below the coin's usual drift. The fall is larger the wider the day's range and the nearer its close to the high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
