---
line: 7.b inconclusive
backtest: 020-04_support-breakdown-continues-down_1d
idea tested: 020-04_support-breakdown-continues-down
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3369 USD
---
## Findings
- **F1:** The tested move is on the predicted side but tiny. On 1,612 short cases the unusual 5-day fall is +0.20 % (t 0.73), a strength of 0.017 of the coin's usual 10.6 % move, about a third of the 0.05 that real ideas show (findings F10). After the coins' own −0.58 % drift the total move is −0.39 %, about −2 times the 0.19 % cost of a trade.
- **F2:** The idea's grading is absent, not just weak, so more cases cannot pass the plan's check. The larger-forecast half falls 0.04 % less than the smaller half. Among cases under the 50-day average, the Spearman correlation of |forecast| with the 5-day unusual fall is 0.003 (p 0.93). The forecast terciles give +0.64 %, +0.86 % and +0.40 %, with the strongest third the weakest.
- **F3:** What fall there is comes from the coin's own downtrend, not from the broken level. The 924 cases below the 50-day average fall +0.63 % more than usual over 5 days (t 1.77). But any grid bar below that average falls +0.38 % anyway (t 1.45, 1,477 cases). The signal minus that baseline is +0.25 % (Welch t 0.56). The 380 cases above the average go the wrong way: −0.90 % (t −1.77).
- **F4:** The sign follows the market's year, not the coins. The 5-day unusual fall is +2.7 % in 2018 (t 3.19) and +2.1 % in 2022 (t 3.00), against −2.9 % in 2021 (t −2.88) and −0.8 % in 2020. By contrast every coin's own t lies between −0.45 and 0.79, so a strong bear market drowns any effect of the level.
- **F5:** Other horizons do not rescue it. Pooled t is −0.65 at 1 day, −1.12 at 3 days, 1.35 at 10 days and 1.13 at 20 days. The only large 20-day values are opposite per coin: ZEC t 3.35 and XRP t −2.21.

## Ideas
- No ideas: The small fall after a support break is the coins' own downtrend: an ordinary bar below the 50-day average falls about as much (difference t 0.56). The break has no grading of its own (rho 0.003, larger half below smaller), so a rerun on more coins would stay inconclusive. Even if confirmed, its 0.20 % per case only matches a 0.19 % trade cost and its total move is negative, so no amended version is supported.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
