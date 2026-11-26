---
line: 7.g patterns
backtest: 064-01_rising-agitated-volume-shrink-rises_1d
idea tested: 064-01_rising-agitated-volume-shrink-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3834 USD
---
## Findings
- **F1:** Among bars in the choppy 60-day trend (60-day return between -10 % and +10 %), the coin's 20-day return predicts its excess 5-day return. The slope is +4.5 % per standard deviation, with t 4.65 on 125 non-overlapping cases, or t 2.51 with the cases of one day taken together (65 days). It stands out among the roughly 90 regressions examined.
- **F2:** Among bars whose 20-day return lies within ±10 %, the excess 5-day return rises across the 20-day-return quintiles: -1.85 %, -0.37 %, +0.39 %, +0.87 %, +4.60 % (about 103 cases each). The slope is positive in every year: t_day 0.96 in 2018, 1.36 in 2019, 2.11 in 2020 and 1.73 in 2021. It holds whether the coin swings more than usual (t_day 2.35, 92 cases) or less (t_day 2.20, 210 cases).
- **F3:** Inside the rising agitated profile, the 30-day volume log-ratio has a negative slope over its whole range, not only on its shrinking half. The slope is -2.9 % of excess 5-day return per standard deviation, t -2.14, or t_day -1.47 over 53 days, on 140 cases.
- **F4:** Across the same profile's volume-ratio quintiles, the excess 5-day return goes from +3.20 % (most shrunk) to -3.41 % (most grown), with 28 cases each. The tested forecast is clipped at 0, so its book never uses the grown-volume half.
- **F5:** The same slope is flat in the rising calm profile: -0.6 %, t -0.68, on 178 cases. When the 20-day return is above +10 %, the slope is strongly negative in 2020 (t_day -4.16) and 2021 (t_day -3.13) but positive in 2019 (t_day +0.91). The volume effect is therefore concentrated in the agitated rising market and in two of the four years.
- **F6:** The tested book pays little. Its Sharpe is 0.29 against holding's 0.57, its yearly return is +1.3 % and it is in a position on 8 % of coin-days. The per-case move (+2.34 % total over 5 days) is 12 times the 0.19 % cost of a trade, so its weakness comes from how rarely it is in the market, not from costs.

## Ideas
- `064-01.g2_rising-agitated-volume-growth-fades` (from F3, F4, F5): In a rising, agitated market, the more a coin's total volume over the last 30 days has grown against the 30 days before, the lower its return over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `064-01.g1_choppy-market-20-day-continuation` (from F1, F2): In a choppy market, the higher a coin's return over the last 20 days, the higher its return over the next 5 days, and the lower that 20-day return, the lower the next 5 days' return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
