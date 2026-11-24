---
line: 7.g patterns
backtest: 031-02.b1_wide-flat-day-continues-uprun_1d
idea tested: 031-02.b1_wide-flat-day-continues-uprun
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5915 USD
---
## Findings
- **F1:** The day's own push carries the next 10 days. A day whose rise is large against the coin's recent volatility is followed by an unusual rise. After a 1-day move above 2.5 of the coin's 20-day daily standard deviation, the 10-day excess return is +4.33 % (t 2.24, 194 cases, 129 days, strength 0.24). Between 1.5 and 2.5 it is +2.35 % (t 2.19, 553 cases, 346 days). In the middle band (−1.5 to 1.5) it is −0.01 % (t −0.01, 1402 cases). The graded slope of the 10-day excess on the day's z, over up days, is +0.024 per unit (t 1.99, 1387 cases, 493 days), well above the 0.19 % cost of a trade.
- **F2:** The same continuation shows in the wide, strong-bodied up days that the tested idea left out. Wide days (range at least 1.5 times the 20-day mean) after a 5-day rise, with a body more than half the range, are followed by +2.69 % of 10-day excess (t 2.48, 461 cases, 305 days, strength 0.14). The wide flat days the idea used give +3.87 % (t 1.77, 62 cases, 55 days). Narrow flat days after a rise give −1.09 % (t −1.14, 242 cases).
- **F3:** The up-day continuation is uneven across years and coins, so it is a regime-bound effect, not a constant one.
- **F4:** The signed body of the day, measured in units of the coin's 20-day mean range, grades the next 10 days in the same direction as F1. On up days the slope is +0.035 per unit (t 1.88, 1453 cases, 506 days). Bodies above 1.0 mean range give +3.2 % excess against −0.6 % to −1.5 % for small bodies. On down days the slope is −0.019 (t −1.89, 1461 cases, 491 days), so deeper down bodies precede a mild rebound, not a continuation.
- **F5:** The next day after a Friday is the strongest of the week for these coins: +0.42 % (t 2.90 with the day's coins pooled, 414 days). It is positive in every year from 2018 to 2025, from 0.00 % to +0.78 %. Monday and Wednesday are slightly negative (−0.12 %, −0.18 %).
- **F6:** The tested book's gain is concentrated. Its 10 best days carry 92 % of its summed daily return over 2898 days, and it is in a position on only 7 % of coin-days. This matches the 77-case, t 0.93 verdict: a few cases, mostly from 2024–2025 (wide flat up-days: +14.1 % in 2024, +9.5 % in 2025, about 0 % in 2019–2021).

## Ideas
- `031-02.b1.g1_strong-up-day-carries-forward` (from F1, F3): After a day on which a coin closes far above its open relative to its own recent daily volatility, the coin keeps rising more than usual over the next 10 days. The larger that day's rise against its 20-day volatility, the larger the further rise.
- `031-02.b1.g2_wide-strong-day-continues-run` (from F2, F4, F3): After a wide-range day on which a coin that has risen over the past 5 days closes well above its open, the coin rises more than usual over the next 10 days. The larger the day's body measured against its average daily range over the past 20 days, the larger the further rise.
- `031-02.b1.g3_deep-down-day-partial-rebound` (from F4): After a day on which a coin closes far below its open relative to its average daily range over the past 20 days, the coin recovers part of that drop over the next 10 days. The deeper that day's body, the larger the recovery.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
