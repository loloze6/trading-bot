---
line: 7.g patterns
backtest: 031-02.b1.b1.b1_wide-flat-uprun-three-day_1d
idea tested: 031-02.b1.b1.b1_wide-flat-uprun-three-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5012 USD
---
## Findings
- **F1:** Inside 6-day up-runs (6-day rise at least 0.5 of its 20-day volatility), the 3-day unusual move rises steadily with the day's range against its 20-day mean range. The bins run from 0–0.8 through 0.8–1.2, 1.2–1.7, 1.7–2.5 to 2.5 and above, and the move goes -0.02 %, +0.19 %, +0.90 % (t 2.93, 796 days), +1.66 % (t 3.73, 528 days), +3.21 % (t 3.10, 270 days). Strength climbs the same way: 0.00, 0.03, 0.09, 0.19, 0.27.
- **F2:** The follow-through after a wide day in an up-run does not need a flat close. Wide days (range at least 1.5x the 20-day mean) in a 6-day rise with a large body (flatness under 0.5) give +1.22 % unusual over 3 days (t 2.56, 1331 cases, 648 days). Every flatness bin from 0 to 0.9 gives between +1.22 % and +1.58 % (t 1.7 to 2.7), so there are about 10 times the cases of the tested flat-only situation (169 cases).
- **F3:** The tested flat wide day after a rise is a stronger tail of the same effect: +3.63 % unusual over 3 days (t 3.56, 169 cases, 129 days, strength 0.40). Narrow flat days in up-runs give -0.23 % (t -0.72, 999 cases). Wide flat days after a fall give +0.60 % (t 0.44, 77 cases).
- **F4:** In down-runs the range does not grade the next 3 days. Wide days after a 6-day fall show no reversal and no continuation by range bin: -0.24 %, -0.09 %, +0.36 %, -0.68 %, +0.71 %, all with |t| < 1. The effect is one-sided, on up-runs.
- **F5:** On wide days, the 3-day unusual move grows with the 6-day rise measured in units of volatility. The bins give -0.95 % (t -1.68) for -1.5 to -0.5, +0.03 % around 0, +1.04 % (t 2.46) for 0.5 to 1.5, +2.16 % (t 3.84) for 1.5 to 2.5, and +3.44 % (t 2.45) above 2.5. On narrow days the same bins stay near 0 up to 2.5: -0.28 %, -0.43 %, -0.09 %, +0.48 %.
- **F6:** On wide days in a 6-day rise, the 3-day unusual move also grows with the 20-day rise: -0.30 % (t -0.34) when it is negative, +1.10 % (t 2.56) for 0–20 %, +2.19 % (t 3.69) for 20–50 %, +3.12 % (t 2.33) above 50 %.
- **F7:** In up-runs, the 3-day unusual move grows with the day's volume against its 20-day mean volume: -0.02 % below 0.8x, +0.50 % (t 1.83) for 0.8–1.2x, +0.75 % (t 2.58) for 1.2–2x, +1.63 % (t 2.82) above 2x.
- **F8:** The wide-day up-run effect is not stable by year. It is positive with t ≥ 2.4 in 2020 and 2024, but -1.33 % in 2018, -0.58 % in 2022 and +0.26 % in 2025, and it is positive in 18 of 19 coins (only UNI at -0.02 %). It holds in every volatility tercile: +1.47 %, +1.53 %, +2.47 %, each with t ≥ 2.5.
- **F9:** The tested book failed only on activity: 0.0085 trades per day against the rule's 0.01, in a position on 4 % of the coins' days. The wider situation in F2 has an unusual move of about 1.2 % per case against a trade cost of 0.22 %.

## Ideas
- `031-02.b1.b1.b1.g1_wide-day-extends-up-run` (from F1, F2, F3, F4, F9): After a coin has risen over the past 6 days, the wider a day's high-low range compared with its average daily range over the past 20 days, the larger the coin's further rise over the next 3 days, whatever the size of the day's body.
- `031-02.b1.b1.b1.g2_wide-day-after-long-climb` (from F5, F6, F8): On a day whose range is wide compared with its 20-day average range, the larger the coin's rise over the past 20 days, the larger its further rise over the next 3 days.
- `031-02.b1.b1.b1.g3_heavy-volume-extends-up-run` (from F7, F1): After a coin has risen over the past 6 days, the higher a day's traded volume compared with its average daily volume over the past 20 days, the larger the coin's further rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
