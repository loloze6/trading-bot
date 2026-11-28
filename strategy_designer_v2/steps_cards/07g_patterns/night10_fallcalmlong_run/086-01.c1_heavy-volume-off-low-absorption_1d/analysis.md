---
line: 7.g patterns
backtest: 086-01.c1_heavy-volume-off-low-absorption_1d
idea tested: 086-01.c1_heavy-volume-off-low-absorption
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3935 USD
---
## Findings
- **F1:** In falling calm markets the coin's climb off its 20-day low predicts its unusual 5-day move: the slope is +2.74 % per standard deviation of the climb (t 2.80, cases of one day together, 121 cases on 83 days), with a Spearman correlation positive on all five 5-day grid offsets (0.29, 0.37, 0.20, 0.15, 0.28, about 140 cases each), while outside the profile it is -0.005.
- **F2:** The coin's 10-day return carries the same graded effect in falling calm markets: slope +2.21 % per standard deviation (t 2.45, 129 cases on 87 days), Spearman 0.16 to 0.32 on the five offsets and 0.006 outside the profile; the distance below the 10-day high gives t 2.20 (129 cases, 87 days).
- **F3:** The tested idea's own inputs carry nothing: the unusual 5-day move after its cases is -0.41 % (t -0.71, 340 cases on 268 days); the volume ratio's Spearman with the in-profile 5-day move is 0.11, close location's is 0.08, and the 5-day volume ratio's slope t is 0.06 (118 cases).
- **F4:** The tested idea's move is smaller than the cost of a trade: a total move of +0.19 % per case against a cost of 0.31 % (0.6 times). The climb in F1 is far larger: 2.74 % per standard deviation is about 9 times that cost.
- **F5:** The weak end of the recent move drives the effect: the lowest tercile of the volatility-scaled 5-day return has an unusual move of -5.03 % (40 cases), against +0.20 % (40) for the middle tercile and +0.04 % (41) for the top. That lowest tercile is negative in ETH (-6.8 %), XMR (-6.9 %) and ZEC (-2.2 %), and in 2018 (-7.3 %) and 2019 (-7.8 %).
- **F6:** The top tercile of the distance from the 20-day high (scaled by volatility, closest to the high) has an unusual 5-day move of +1.60 % (41 cases) against -3.21 % for both the deep and the middle terciles. It is positive in ETH, XMR and ZEC and in 2018, 2020 and 2021, and negative in BCH and in 2019.
- **F7:** The falling calm profile on its own earns less than the coin's drift: its 5-day grid has an unusual move of -0.83 % (146 cases, t -1.00). The year splits are unstable: 2019 is -2.94 % (t -2.91, 62 cases) and 2021 is +3.44 % (t 2.13, 28 cases). No weekday stands out (largest |t| 1.76).

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `086-01.c1.g1_calm-decline-climb-off-low` (from F1, F5, F6, F7): In a falling, calm market, the further a coin has climbed above its lowest close of the past 20 days, the larger its rise over the next 5 days.
- `086-01.c1.g2_calm-decline-ten-day-strength` (from F2, F4, F5): In a falling, calm market, the higher a coin's 10-day return, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
