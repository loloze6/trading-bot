---
line: 7.g patterns
backtest: 003-01_thin-volume-rise-reverses_1d
idea tested: 003-01_thin-volume-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4616 USD
---
## Findings
- **F1:** The tested short fought a continuation. The top quintile of one-day moves in 20-day volatility units was followed by a mean excess 5-day return of +0.0160 (t 3.31, n 598, non-overlapping 5-day grid). On up days only, the largest-rise quartile gave +0.0180 (t 2.91, n 356), and the rise's size ranked positively with the excess 5-day return (Spearman rho 0.080, p 0.0026, n 1422). The effect held in both halves: 2018-2021 gave +0.0261 (t 3.42, n 256) and 2022-2025 gave +0.0085 (t 1.36, n 342).
- **F2:** Heavy volume is what carries the continuation of large rises, and thin volume does not reverse them. Across the larger half of up days, by volume tercile against the prior 30-day mean:
- **F3:** The day's log volume ratio against its prior 30-day mean ranks positively with the coin's excess 5-day return on all days (rho 0.064, p 0.0005, n 2987). The relation appears on both day types: up days rho 0.070 (p 0.008) and down days rho 0.057 (p 0.023). By volume quintile the excess return runs −0.0073, −0.0052, −0.0044, +0.0060, +0.0058. It is uneven across time and coins:
- **F4:** The book sat short at a near-constant size, regardless of how large the rise was. Its mean position on active up days ran −0.40, −0.34, −0.36 and −0.33 across the rise quartiles, so it was fully exposed to the continuation in F1. Its daily mean return was negative or about zero on every coin (BTC −0.00050, ETH −0.00046, XMR −0.00044), and its Sharpe was −0.54.
- **F5:** Weekday effects looked strong when pooled but are unstable, so they are not counted as a finding. Pooled, Monday gave +0.0143 (t 2.89) and Sunday −0.0118 (t −2.19). Between halves, Wednesday went from −0.0229 (t −3.19) to −0.0014, and Sunday flipped from +0.0121 to −0.0263.

## Ideas
- `003-01_thin-volume-rise-reverses.g1_heavy-volume-rises-keep-going` (from F1, F2, F4): When a coin rises sharply over one day on volume above its own 30-day average daily volume, it keeps rising over the next 5 days. The larger the rise in units of its 20-day volatility and the heavier the volume against that average, the larger the further gain.
- `003-01_thin-volume-rise-reverses.g2_large-daily-moves-continue` (from F1, F4): The larger a coin's one-day return in units of its 20-day return volatility, the higher its return over the next 5 days, in the direction of that day's move.
- `003-01_thin-volume-rise-reverses.g3_relative-volume-leads-returns` (from F3, F2): The heavier a day's volume against the coin's prior 30-day average daily volume, the higher the coin's return over the next 5 days, and the thinner that volume, the lower that return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
