---
line: 7.g patterns
backtest: 075-01.d3_heavy-volume-deep-fall-rebound_1d
idea tested: 075-01.d3_heavy-volume-deep-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4265 USD
---
## Findings
- **F1:** The tested idea's edge comes from volume, not from the depth of the fall: on down days, the heaviest-volume fifth (volume about 1.8 times its 20-day mean) was followed by a next-day excess return of +1.22 % (t 2.89, 1117 cases), while the other four fifths ranged from -0.08 % to +0.25 % (t at most 1.05); that heaviest fifth was positive in each year, 2018 +1.41 %, 2019 +0.44 %, 2020 +1.80 % and 2021 +1.83 %.
- **F2:** Up days are graded by volume in the direction the brief gives for its light side: their next-day excess return runs from -0.62 % (t -2.50) for the lightest-volume fifth (volume about 0.38 times its 20-day mean) through -0.51 % (t -2.41), -0.40 % and -0.21 % to -0.05 % (t -0.15) for the heaviest fifth, with about 1163 cases in each fifth.
- **F3:** Up days are also graded by the size of the rise: the next-day excess return goes from -0.57 % (t -2.52) after the smallest rises (0.10 of the 30-day daily swing) through -0.30 %, -0.35 % and -0.17 % to +0.02 % after the largest rises (1.67 swings), with about 1050 cases in each fifth.
- **F4:** The two gradings on up days add up: light volume with a small rise was followed by -0.64 % (t -2.42, 876 cases), while heavy volume with a large rise was followed by 0.00 % (t 0.00, 1014 cases).
- **F5:** The fade of up days is absent in a rising market and present elsewhere: up days in a rising 60-day trend were followed by +0.19 % (t 0.63, 1386 cases), against -0.57 % in a falling trend (t -1.89, 1296 cases) and -0.48 % in a choppy one (t -1.59, 503 cases); the weakest fifth of up days (light volume, small rise) fell -0.89 % in agitated markets (t -2.04, 298 cases) against -0.39 % in calm ones (t -1.37, 752 cases).
- **F6:** The heavy-volume down-day effect lasts only one day: on a 3-day grid, down days sorted by the depth of their fall had excess returns of +0.64 % down to -0.16 %, all with t under 0.61; in the book, the gain per held bar was 0.80 % in the deepest-fall fifth against 0.04 % in the shallowest.
- **F7:** The other angles did not stand out after this many looks: weekday means had |t| ≤ 1.47, the widest-range fifth of days had +0.71 % (t 1.83), and down days that closed near their high had -0.37 % (t -1.06).
- **F8:** Against costs, the light-volume up-day fade moves about 0.6 % per case over one day, nearly three times the 0.22 % a trade cost, and it is a short-side effect where the profile map is thin (choppy agitated short: 0 strategies).

## Ideas
- `075-01.d3.g1_light-volume-rise-fades` (from F2, F4, F8): The lighter a coin's volume on a day that closed higher, relative to its own average daily volume over the past 20 days, the larger its fall over the next day.
- `075-01.d3.g2_falling-market-thin-rally-fade` (from F2, F5): In a falling market, the lighter a coin's volume on a day that closed higher, relative to its own average daily volume over the past 20 days, the larger its fall over the next day.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `075-01.d3.g3_timid-up-day-fades` (from F3, F4, F5): The smaller a coin's rise on a day that closed higher, measured against its 30-day daily swing, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
