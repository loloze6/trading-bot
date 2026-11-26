---
line: 7.g patterns
backtest: 074-01.b1_low-close-nearness-rebound_1d
idea tested: 074-01.b1_low-close-nearness-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4221 USD
---
## Findings
- **F1:** In a rising calm market, the rebound after a day that closes in the bottom quarter of its range grows with the day's width against the 30-day swing. The next-day unusual move is -0.45 % (t -0.75, 50 days) at 1 to 1.5 times the swing, +0.85 % (t 0.96, 42 days) at 1.5 to 2, +2.17 % (t 2.59, 37 days) at 2 to 3, and +3.36 % (t 4.31, 20 days) above 3.
- **F2:** In a rising calm market, nearness to the low matters only on wide days. Above 3 times the swing, the next-day unusual move is +3.36 % (t 4.31) for a close in the bottom quarter, +0.71 % (t 0.70, 24 days) for the next quarter up, and -1.49 % (t -1.13, 22 days) for the quarter below the middle.
- **F3:** A single score, the day's width against its swing times the close's nearness to its low, grades the next-day move in rising calm bars. Only its top fifth stands out at +1.02 % (t 2.36, 178 days, 342 cases); the four lower fifths sit between -0.07 % and +0.37 %, every t under 1.2.
- **F4:** In the top fifth of that score, the 2-day unusual move (+1.03 %, t 1.89) is no larger than the 1-day move (+1.02 %), so the whole rebound comes on the first day.
- **F5:** By year, the top fifth's next-day move is +2.69 % in 2018 (11 days), -0.00 % in 2019 (41 days), +1.65 % in 2020 (t 3.96, 65 days) and +0.84 % in 2021 (61 days), so 2019 carries none of the effect.
- **F6:** The same wide, low-close rebound also appears outside rising calm, but it is weaker there. Outside the profile, days at least 2 times the swing closing in the bottom quarter give +1.20 % (t 4.07, 416 cases); inside it they give +2.52 % (t 4.95, 81 cases). Outside the profile the map already holds this pattern in its agitated and falling-agitated long cells.
- **F7:** In a falling 60-day trend, a day closing in the top quarter of its range is followed by a next-day fall that grows with the day's width. The move is +0.59 % below 1 times the swing, -1.44 % (t -1.79, 41 days) at 2 to 3, and -3.30 % (t -2.29, 15 days) above 3. For days at least 2 times the swing it is negative in every year, from -0.75 % to -3.70 %. This is the source brief 060's situation, and the map already holds it as 060-01.g1.d2.d1 in falling agitated short, so it is left out.
- **F8:** In rising calm bars, a bar closing on a Thursday is followed by +1.41 % the next day (t 4.84, 271 cases) and a Wednesday bar by -0.83 % (t -2.71, 280). The map already holds this as 045-01 (rising market late week gain), so it is left out.
- **F9:** The tested book was in its regime on only 87 of 9,986 bars. It failed on trades per day (0.0095 against at least 0.01), even though its Sharpe was 1.05 and its Calmar 1.16.

## Ideas
- `074-01.b1.g1_width-times-low-close-rebound` (from F1, F2, F3, F4, F9): In a rising, calm market, a day that is wide against the coin's 30-day swing of daily returns and that closes near its low is followed by a rise over the next day. The rise is larger the wider the day against that swing and the nearer its close to the low, both together.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
