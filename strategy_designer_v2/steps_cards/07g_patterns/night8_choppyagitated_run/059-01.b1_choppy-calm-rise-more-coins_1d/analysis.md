---
line: 7.g patterns
backtest: 059-01.b1_choppy-calm-rise-more-coins_1d
idea tested: 059-01.b1_choppy-calm-rise-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4093 USD
---
## Findings
- **F1:** Inside the choppy calm profile, the excess 7-day return is not graded with the scaled weekly rise: by quintile of the scaled 7-day rise it is +1.3 %, −1.4 %, −2.1 %, −4.0 % and then +7.5 % (day-clustered t 0.44, −0.49, −1.31, −1.71, 1.97; 25 to 35 cases on 17 to 24 days each), so the whole effect sits in the top fifth.
- **F2:** Even that top fifth is unstable by year: on cases with a positive scaled rise in profile, 2018 had −8.3 % (t −2.83, 13 cases) and 2019 had −2.8 % (t −1.77, 22 cases). Only 2020 (+3.0 %, t 1.04) and 2021 (+7.7 %, t 2.36, 25 cases) were positive, and the top quintile's gain in 2021 (+12.7 %, t 2.30) rests on 6 days.
- **F3:** Splitting by agitation instead of the full profile, the weekly rise continues in calm markets across all trends. In calm markets the excess 7-day return by quintile of the scaled weekly rise is −0.7 %, −0.1 %, −0.6 %, +0.9 % and +4.4 % (top t 3.03). In agitated markets it is −2.8 % to −2.0 % (top t −1.11). Three caveats apply: agitation here is a 60-day rank of the 30-day swing, not the profile's 1-year rank; the t is not day-clustered; and in-profile day-clustering cut a comparable t from 2.72 to 1.97.
- **F4:** In a falling, agitated market, the next day's excess return falls steadily as the day's scaled move rises: by quintile of the 1-day move it is +1.2 %, +1.3 %, −1.1 %, −1.4 % and −1.4 % (day-clustered t 1.49, 1.80, −1.26, −2.34, −2.03). After the largest rises, the excess return over the next 3 days is −3.6 % (t −1.74). The choppy agitated cell shows the same next-day giveback after the largest rises (−1.4 %, t −2.29), while rising agitated does not (+0.6 %, t 0.96).
- **F5:** Over all coins, after the weakest fifth of scaled 1-day moves, the next day's excess return is +0.76 % (t 5.25, 1653 cases). This is the rebound after a fall the portfolio already holds many times (12 falling agitated long strategies), so it is not a discovery.
- **F6:** Weekday next-day excess returns, Wednesday −0.44 % (t −2.60) and Friday +0.37 % (t 2.85), do not stand out among the 7 days and the many angles looked at. The late-week gain is already held (045-01).

## Ideas
- `059-01.b1.g1_calm-market-weekly-rise-continues` (from F3, F1, F2): In a calm market, the larger a coin's rise over the past 7 days against its usual daily swing over the past 30 days, the larger its further rise over the next 7 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `059-01.b1.g2_falling-agitated-rally-fades` (from F4): In a falling, agitated market, the larger a coin's rise on a day against its usual daily swing over the past 30 days, the more it falls back over the next 1 to 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
