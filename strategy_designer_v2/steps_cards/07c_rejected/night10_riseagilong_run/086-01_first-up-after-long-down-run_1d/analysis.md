---
line: 7.c no effect
backtest: 086-01_first-up-after-long-down-run_1d
idea tested: 086-01_first-up-after-long-down-run
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4404 USD
---
## Findings
- **F1:** The tested event shows no effect at any horizon. In rising agitated bars, the first up close after 2 or more down closes leaves an unusual move of -0.71 % over 1 day (t -1.07, 119 days), -0.62 % over 2 days (t -0.74), -0.81 % over 5 days (t -0.50, 160 cases on 110 days) and -0.33 % over 10 days (t -0.11). This matches step 5's -0.13 % (t -0.16, 390 cases).
- **F2:** The move does not grow with the run's length; the longest runs come out worst. Over 5 days the unusual move is -0.66 % after 1 down day (154 cases), +0.08 % after 2 (89), -1.43 % after 3 (52) and -4.24 % after 4 or more (23 cases, t -1.27). Step 5's run-length slope is also negative (-0.0013).
- **F3:** The depth of the run, measured against the 30-day swing, points the opposite way to the brief. Its slope on the unusual move is negative at every horizon: t -1.24 over 2 days, -1.34 over 3 days and -1.47 over 5 days (204 cases). By tercile over 5 days, the deep runs give -0.89 % (t -0.47), against +3.21 % for the middle tercile (t 1.32).
- **F4:** What the market grades instead is the size of the up day itself. Its slope on the unusual move is positive at every horizon: t 1.26 over 2 days, 1.48 over 3 days and 0.96 over 5 days. The top quartile of up days gives +2.50 % over 2 days (t 1.69) and +2.82 % over 3 days (t 1.59, 71 cases); the middle quartiles give -0.6 % to -1.4 %. For the top third over 3 days: +2.04 % (t 1.41, 70 days) against -0.24 % (t -0.26) for the rest.
- **F5:** The big-up-day effect is uneven, so it is fragile. Over 3 days it is positive on LTC (+3.8 %, 37 cases), XRP (+4.5 %, 15) and ETH (+1.0 %, 24) but negative on XMR (-2.5 %, 17). By year it is positive in 2017 (+6.1 %), 2018 and 2021 (+4.5 %), and negative in 2019 and 2020 (-0.7 %, 33 cases).
- **F6:** Within the events, a stronger past 5-day return (the dip smaller than the prior rise) goes with a larger rise afterwards. The slope's t is 1.70 over 2 days, 1.66 over 3 days and 1.85 over 5 days (204 cases). This is continuation, not recovery from deep selling.
- **F7:** The size of the idea cannot pay a trade. The total move per case is +0.52 % against a trade cost of 0.26 %, and almost all of it is the coins' drift (+0.65 %). The book's Sharpe of 0.28 falls 0.57 below holding's, and its Calmar is 0.11.

## Ideas
- `086-01.c1_forceful-turn-day-continues` (from F4, F5, F1): In a rising, agitated market, on the first up day after a run of consecutive down days, the coin rises over the next 3 days, and the larger that up day against the coin's usual daily swing over the past 30 days, the larger that rise.
- `086-01.c2_shallow-pullback-turn-continues` (from F6, F3, F2): In a rising, agitated market, on the first up day after a run of consecutive down days, the coin rises over the next 5 days, and the higher its 5-day return against its usual daily swing over the past 30 days (the shallower the dip within the rise), the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
