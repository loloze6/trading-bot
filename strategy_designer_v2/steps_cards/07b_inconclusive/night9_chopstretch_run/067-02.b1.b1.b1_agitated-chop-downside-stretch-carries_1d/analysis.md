---
line: 7.b inconclusive
backtest: 067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d
idea tested: 067-02.b1.b1.b1_agitated-chop-downside-stretch-carries
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3897 USD
---
## Findings
- **F1:** Inside the tested profile (choppy agitated, regime 'unknown'), coins fell whichever side of the average they closed on, so the market's own fall swamps the stretch: on the 5-day grid of folds B and C, closes below the average were followed by an excess of -4.7 % (t -2.29, 43 cases) and closes above it by -3.6 % (t -2.17, 22 cases), and the bars actually traded gave a mean excess of -9.6 % (t -3.41, 24 cases), which a short collects without any carry.
- **F2:** Inside the profile, the grading the idea needs is absent, matching step 5's failed size check (larger half minus smaller half -0.0043). The below-average cases split into terciles give an excess of -12.3 % for the deepest (t -2.62, 15 cases), +0.6 % for the middle (14) and -1.8 % for the shallowest (14). The result also flips by year (below side 2020 -13.3 %, 2021 +1.2 %) and by coin (ZEC below +0.25 %, 11 cases).
- **F3:** Choppy agitated bars are rare: 319 of 6,951 bars (4.6 %) in folds B and C. Step 5's result is on the predicted side but small (weighted excess +1.2 %, t 0.65, 133 cases on 93 days), with a size of -0.13 % (t -0.19) per case. On these six coins, more cases can only come from adding coins.
- **F4:** Across the brief's whole choppy market (60-day return within ±10 %, calm or agitated), the stretch carries forward on both sides and in a graded way. Over 5 days the carry is +3.3 % (t 3.28, 125 cases, Spearman of stretch with excess 0.31), and the stretch quintiles run from -8.6 % (lowest) through -3.5 %, -1.9 %, +2.5 % to +4.0 % (highest). Over 10 days the carry is +5.7 % (t 2.75, 62 cases, Spearman 0.38).
- **F5:** The choppy carry is broad. It is positive in every year (2018 +1.5 %, 2019 +1.1 %, 2020 +5.2 %, 2021 +6.1 %) and on every coin (ETH +0.2 % to XRP +8.5 %, Spearman positive on all six). In choppy calm bars it holds on both sides alike: above +2.9 % (t 1.96, 58 cases) and below +2.9 % (t 2.30, 43 cases).
- **F6:** The same 5-day carry is weaker outside the choppy market: +2.7 % in rising markets (t 3.60, 318 cases, Spearman 0.15) and +1.5 % in falling markets (t 2.74, 369 cases, Spearman 0.15). The choppy market is where the stretch says most about what follows (Spearman 0.31).

## Ideas
- `067-02.b1.b1.b1.b1_agitated-chop-downside-more-coins` (from F3, F1): In a choppy, agitated market, the further a coin's close stands below its 20-day average, counted in units of its current 20-day standard deviation of daily returns, the more the coin keeps falling over the next 5 days.
- `067-02.b1.b1.b1.b2_choppy-two-sided-stretch-carry` (from F4, F5, F6, F2): In a choppy market, the further a coin's close stands from its 20-day average, counted in units of its current 20-day standard deviation of daily returns, the more the coin keeps moving the same way over the next 5 days: further up after closes above the average, further down after closes below it.
- `067-02.b1.b1.b1.b3_calm-chop-stretch-carry` (from F5, F1, F4): In a choppy, calm market, the further a coin's close stands from its 20-day average, counted in units of its current 20-day standard deviation of daily returns, the more the coin keeps moving the same way over the next 5 days: further up after closes above the average, further down after closes below it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
