---
line: 7.b inconclusive
backtest: 070-01_calm-decline-run-break-fade_1d
idea tested: 070-01_calm-decline-run-break-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3118 USD
---
## Findings
- **F1:** The test's main measure is on the predicted side but well short of the bar: the next-day unusual move on the 870 short cases is +0.20 % (t 0.98 with cases summed by day, 488 days). In the folds shown here (B and C) it is +0.60 % on 484 cases (t_day 1.98, ordinary t 2.95), so roughly two thirds of the folds' evidence points the right way but does not clear t 2.
- **F2:** The grading the idea claims is there, and the longest runs carry the effect. The next-day unusual move by run length is +0.24 % after 1 down day (226 cases, t_day 0.57), +0.91 % after 2 (125, t_day 1.48), +0.26 % after 3 (75), +1.25 % after 4 (22) and +2.13 % after 5 or more (36, t_day 2.81). Step 5's run ≥3 minus run 1–2 check also passed (+0.64 %).
- **F3:** The result is unclear because the effect varies from one period to the next, which drowns the mean. By year the move is +1.40 % in 2018 (216 cases, t_day 2.48) and +0.31 % in 2019 (177, t_day 0.83), then −1.02 % in 2020 (44) and −0.45 % in 2021 (47). By window it ranges from +2.19 % (w14, 56 cases) and +1.71 % (w7, 110 cases) down to −2.08 % (w16, 16 cases).
- **F4:** Coin by coin it is positive on all six (ETH +1.34 %, t 2.58; BTC, LTC and XMR about +0.63 %; ZEC +0.44 %; XRP +0.11 %), but each coin has only 56 to 110 cases. So the effect is not confined to one coin; the cases per coin are too few.
- **F5:** On longer horizons the move holds its sign but loses certainty: +0.62 % over 2 days (t_day 1.42), +0.64 % over 3 days (t_day 1.09) and +0.75 % over 5 days (t_day 0.99). The exception is runs of 5 or more days, where the 3-day move is +4.06 % (34 cases, t_day 3.02).
- **F6:** The effect is small against what a trade costs. Per case the total move is +0.07 %, 0.4 times the 0.19 % cost of a trade, and the unusual move is +0.20 %, 1.0 times the cost (strength 0.044 of a 4.73 % usual daily move). The book's Sharpe is 0.30 against holding's 0.57, and its yearly return is +1.3 %. Only more evidence can show whether this size is real.

## Ideas
- `070-01.b1_calm-decline-fade-more-coins` (from F1, F2, F3, F4): In a falling, calm market, a day that closes up after an unbroken run of down days is followed by a fall over the next day, and the longer that run of down days, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
