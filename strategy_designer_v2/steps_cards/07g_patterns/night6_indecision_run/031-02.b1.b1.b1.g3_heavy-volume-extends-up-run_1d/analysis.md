---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d
idea tested: 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4467 USD
---
## Findings
- **F1:** During 6-day rises on days of above-average volume, the 3-day excess return over holding grows with the 6-day return measured in 20-day daily volatility: the top tercile of that run strength is followed by +2.43 % (t 3.37 with one day's cases taken together, 713 cases, strength 0.238), the middle tercile by +0.24 % (t 0.51, 712 cases) and the bottom tercile by −0.16 % (t −0.36, 713 cases).
- **F2:** Across all grid bars, the 6-day return deciles show the same direction but weaker: the top decile (6-day rise above 15 %) is followed by +0.94 % 3-day excess (t 1.55, 1156 cases), and the deciles between −2 % and +5 % sit between −0.79 % and −0.04 %.
- **F3:** Inside 6-day rises, the day's range against its 20-day average range carries the volume signal's information: the widest-range quintile is followed by +1.34 % 3-day excess (t 2.13, 1005 cases, strength 0.130), the other four quintiles lie between −0.19 % and +0.22 %. Taken together in one regression, neither log volume ratio (t 1.11) nor log range ratio (t 1.24) stands alone.
- **F4:** Volume adds nothing outside up runs: in 6-day falls the volume-ratio quintiles are followed by 3-day excess returns from −0.66 % to +0.14 %, all with |t| ≤ 1.43, and the joint volume t is −0.85.
- **F5:** The heavy-volume up-run effect is unstable by year: its 3-day excess is negative in 2018 (−2.27 %, 91 cases), 2022 (−0.64 %, 222) and 2025 (−0.95 %, 340), and positive in the other five years (up to +2.81 % in 2021, 254 cases), so it pays in bull years.
- **F6:** The book's gain is concentrated in rare days: its days above its own 95th percentile (+1.61 %) sum to 211 % of its total summed daily gain. Its daily returns correlate 0.59 with the coins' daily returns.
- **F7:** The brief's own pattern points the other way but cannot be told from chance: wide-range (over 1.5 times the 20-day average range), flat-body days after a 6-day rise are followed by +1.84 % 3-day excess (t 1.56, 107 cases), not by a move back.

## Ideas
- `031-02.b1.b1.b1.g3.g1_vol-scaled-run-strength-continues` (from F1, F2, F5): The larger a coin's 6-day rise measured in units of its own daily volatility over the past 20 days, the larger its further rise over the next 3 days.
- `031-02.b1.b1.b1.g3.g2_wide-range-extends-up-run` (from F3, F4, F7): While a coin has risen over the past 6 days, the wider a day's high-to-low range compared with its average daily range over the past 20 days, the larger the coin's further rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
