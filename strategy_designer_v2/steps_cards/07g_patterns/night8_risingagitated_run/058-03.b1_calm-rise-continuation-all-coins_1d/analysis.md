---
line: 7.g patterns
backtest: 058-03.b1_calm-rise-continuation-all-coins_1d
idea tested: 058-03.b1_calm-rise-continuation-all-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4242 USD
---
## Findings
- **F1:** In choppy calm markets (60-day return between −10 % and +10 %, 30-day swing at or below the coin's median), the slope of the coin's excess return on its distance from the 20-day average, measured in the coin's own swings, is positive at every horizon tested: over 3 days 0.012 (t 0.75, 191 cases, 92 days), over 5 days 0.107 (t 3.08, 117 cases, 55 days) and over 10 days 0.199 (t 4.72, 58 cases, 28 days), the largest t of all the angles looked at.
- **F2:** Across calm markets that are not rising (choppy calm and falling calm together, 5 days), the move is graded through both sides of the average: quartiles of the swing-scaled distance give −5.7 % (t −2.45), −2.5 %, +1.0 % and +4.1 % (t 2.47), 74–75 cases each. The slope is positive below the average (0.052, t 1.38, 191 cases) and above it (0.059, t 1.92, 108 cases), and positive on all 7 coins with enough cases (0.041 to 0.138, t 1.5 to 2.2).
- **F3:** The same 5-day continuation holds in falling calm markets: slope 0.054, t 2.55, 182 cases, 61 days (over 3 days 0.033, t 2.06). In falling agitated markets it is absent (−0.010, t −0.35, 255 cases). The continuation lives in calm markets, not in every market.
- **F4:** The brief's own effect is not in the data. In rising agitated markets the 5-day slope on distance is +0.014 (t 0.58, 179 cases), and over 10 days +0.006 (t 0.13). The quartiles of distance give −1.7 %, −0.4 %, −2.1 % and +1.1 % excess with no ordering, so the largest distances above the average are followed by no giveback.
- **F5:** The tested rising-calm continuation strengthens with the horizon: the swing-scaled slope is 0.018 over 3 days (t 1.30), 0.050 over 5 days (t 1.96) and 0.125 over 10 days (t 3.22, 97 cases). Inside the backtest's own profile bars, the raw-distance slope over 5 days is weaker (0.082, t 0.93, 329 cases) and its top two quintiles are not ordered (+2.7 % then +2.2 %). The 10-day version is already held (058-03.e1).
- **F6:** By year, the not-rising calm continuation over 5 days is positive in 2018 (t 1.54), 2020 (t 1.50) and 2021 (t 2.10) and flat in 2019 (−0.004, t −0.13). It is not carried by one year.
- **F7:** Other angles did not stand out against the number of tests:

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-03.b1.g1_choppy-calm-stretch-continues` (from F1, F2, F6): In a choppy, calm market, the further a coin's close stands from its 20-day average price, measured in the coin's daily swings over the last 30 days, the further the coin moves the same way over the next 10 days: up when it stands above the average, down when it stands below.
- `058-03.b1.g2_falling-calm-stretch-keeps-falling` (from F3, F2): In a falling, calm market, the further a coin's close stands below its 20-day average price, measured in the coin's daily swings over the last 30 days, the more the coin falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
