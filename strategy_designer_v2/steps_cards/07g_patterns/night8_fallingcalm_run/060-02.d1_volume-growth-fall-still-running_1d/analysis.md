---
line: 7.g patterns
backtest: 060-02.d1_volume-growth-fall-still-running_1d
idea tested: 060-02.d1_volume-growth-fall-still-running
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3943 USD
---
## Findings
- **F1:** Outside the falling market (the "chop" regime, 60-day return at or above -10 %), the last day's return continues over the next 5 days. The 1-day return has a slope of 0.28 on the 5-day excess return (t 3.75, 991 non-overlapping cases). Scaled by the 30-day swing, the lowest quintile of the move is followed by -2.45 % excess and the highest by +3.43 %, with the quintiles between nearly monotone (-0.13 %, +0.17 %, +0.28 %). Taking the sign of the move, the unusual move is +1.22 % per case, a strength of 0.090 (739 cases).
- **F2:** This continuation of the scaled day move holds in calm markets (slope t 4.10, 416 cases) more than in agitated ones (t 2.00, 323 cases). It holds in choppy (t 2.51, 127 cases) and rising (t 2.69, 318 cases) markets but is weaker in falling ones (t 1.79, 401 cases). It is positive in 2019, 2020 and 2021 (t 2.77, 2.00, 2.69) but not in 2018 (t 0.15), and on all six coins, though clearly only on XMR, XRP and ZEC (t 2.3 to 3.2).
- **F3:** In a rising, agitated market, the 30-day volume growth against the 30 days before predicts a lower 5-day return (slope -0.059, t -2.84, 139 cases), the reverse of the falling market's sign. Outside the falling market, the quintile with the most shrunk volume (log ratio -0.59) is followed by +3.99 % excess, against -0.9 % to -0.1 % for the other four. The effect is carried mostly by 2021 (t -4.34); 2019 is weaker (t -1.55) and 2018 and 2020 are near 0.
- **F4:** Inside the tested regime (falling and 20-day return below 0), the forecast's slope is strong only in the middle 20-day-return tercile (t 5.40, 142 cases), against t 0.83 and 1.35 in the two extremes. By year it fades from 2018 (t 3.06) to 2021 (t 0.11). Both sides earn: shorts on volume shrinkage -1.70 % excess (t -2.65, 276 cases) and longs on volume growth +2.20 % (t 2.22, 202 cases).
- **F5:** The book's gain sits on a few days. Its top 10 % of days sum to 4.1 times the whole book's total gain (1,449 days, mean +0.042 % a day, standard deviation 0.95 %), consistent with the Calmar of 0.33 failing while the Sharpe of 0.60 passes.
- **F6:** Weekday differences in the 5-day excess return (Monday +1.70 %, t 2.42; Thursday -1.85 %, t -2.50) do not stand out among the seven weekdays and many angles tested, and are not taken as findings for ideas.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-02.d1.g1_calm-market-day-move-continues` (from F1, F2): In a calm market, a coin's return on its last day, measured against its usual daily swing over the past 30 days, continues over the next 5 days: the larger that day's rise, the larger the rise that follows, and the larger that day's fall, the larger the fall that follows.
- `060-02.d1.g2_rising-agitated-volume-dry-up-rise` (from F3): In a rising, agitated market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
