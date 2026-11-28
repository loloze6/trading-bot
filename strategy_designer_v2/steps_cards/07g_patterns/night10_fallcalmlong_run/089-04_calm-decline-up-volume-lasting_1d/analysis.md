---
line: 7.g patterns
backtest: 089-04_calm-decline-up-volume-lasting_1d
idea tested: 089-04_calm-decline-up-volume-lasting
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3901 USD
---
## Findings
- **F1:** In the falling calm profile, the tested lean has no relation to later returns. The share of the last 20 days' volume on up days has a Spearman rho of -0.019 with the 10-day excess return (57 cases; top tercile -3.73 % against bottom tercile -3.72 %, t -0.00) and 0.071 with the 5-day excess return (121 cases, t 0.52). This agrees with step 5's slope t of -1.08.
- **F2:** In the falling calm profile, the coin's own 10-day return predicts its excess return over the next 3 to 7 days. On non-overlapping grids with day-clustered t, the slope is 0.114 at 3 days (t 2.46 averaged over grid offsets, lowest 2.10, about 222 cases), 0.196 at 5 days (t 2.61, lowest 1.77, about 128 cases) and 0.257 at 7 days (t 2.60, about 89 cases). It weakens to t 1.86 at 10 days.
- **F3:** The F2 relation is graded across the whole range. Sorted into quartiles of the 10-day return (-17.6 %, -4.6 %, +1.3 %, +13.8 %), the falling calm cases have 5-day excess returns of -4.10 %, -2.96 %, +0.26 % and +2.01 %, and total 5-day moves of -2.98 %, -1.79 %, +1.43 % and +3.18 %. The top quartile's total move is about ten times the 0.31 % cost of a trade.
- **F4:** The F2 relation belongs to the falling calm profile. Outside it, the same 5-day slope on the 10-day return is -0.017 (t -0.33, 634 cases on 226 days).
- **F5:** The F2 relation points the same way in every coin and both halves of the explored windows, but only ETH is significant on its own. The 5-day slope is 0.278 for ETH (t 2.43, 48 cases), 0.097 for XMR (t 1.14), 0.116 for ZEC (t 0.76) and 0.031 for BCH (t 0.32). It is 0.142 in w7–w12 (t 1.20, 84 cases) and 0.112 in w13–w18 (t 1.22, 45 cases).
- **F6:** The tested book earns nothing reliable. On its 616 active coin-days the mean daily return is 0.12 % (t 1.13), and its best 5 % of days carry 283 % of its summed gain. Per case its total move (+0.28 %) is below the 0.31 % cost of a trade.
- **F7:** Other angles in the falling calm profile show nothing that stands out:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `089-04.g1_calm-decline-rebound-continuation` (from F2, F3, F4, F5): In a falling, calm market, the higher a coin's 10-day return, the more it rises over the next 5 days: a coin rebounding inside an orderly decline keeps rising in proportion to the rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
