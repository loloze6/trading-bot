---
line: 7.g patterns
backtest: 058-01.g2.d1_volume-dry-up-at-the-lows_1d
idea tested: 058-01.g2.d1_volume-dry-up-at-the-lows
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4098 USD
---
## Findings
- **F1:** Across all coins and windows, the next day's excess return falls steadily with where the day closed in its range. Closes in the bottom fifth of the range were followed by +0.515 % (1,666 cases, day-clustered t 2.10) and closes in the top fifth by −0.371 % (t −1.83). The top-minus-bottom gap was negative in 10 of 12 windows and in every year (2018 −1.04 %, 2019 −0.90 %, 2020 −1.92 %, 2021 −0.37 %).
- **F2:** The fade after a close near the day's high is concentrated in falling agitated markets: −1.083 % the next day (178 cases, t −1.84), and −0.947 % in choppy agitated (45 cases, t −1.49). The same close was followed by +0.456 % in falling calm, +0.079 % in rising agitated and +0.784 % in rising calm. On the profile map the falling agitated short and choppy agitated short cells are empty.
- **F3:** Inside the falling calm profile, the tested forecast's quintiles were graded in the short's favour, from an excess 5-day return of −2.662 % for the strongest fifth (75 cases, t −2.12) to +1.010 % for the weakest. The evidence is not reliable, though: the stronger half had a day-clustered t of only −1.27, and its 5-day excess return went against the short in 4 of 11 windows (w12 +5.68 %, w16 +9.67 %, w17 +4.18 %, w18 +5.82 %). The book's position gain by window swung from +122 % (w14) to −91 % (w16), and the book's Sharpe was 0.13.
- **F4:** Across all profiles, the largest one-day falls (the bottom decile of the day's return scaled by its 20-day swing) were followed by +0.868 % the next day (689 cases, t 3.77). The largest rises were followed by −0.095 % (t −0.42). This long-side rebound is already held by the twelve falling agitated long strategies on the map.
- **F5:** The other angles show nothing that stands out after this many looks. By weekday the extremes were Wednesday −0.504 % (t −2.68) and Thursday +0.358 % (t 2.28), with no reason behind them. The 5-day quintiles by 5-day and 20-day past return were not monotone, and the 5-day excess return showed no gradient by volatility quintile inside the profile (−0.33 % to −1.76 %, all |t| < 1.7).

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g2.d1.g1_falling-agitated-high-close-fade` (from F2, F1): In a falling, agitated market, the closer a coin's close sits to the top of that day's high-low range, the more it falls back over the next day.
- `058-01.g2.d1.g2_daily-close-location-reversal` (from F1): The closer a coin's close sits to the top of that day's high-low range, the lower its return over the next day, and the closer to the bottom, the higher.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
