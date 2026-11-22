---
line: 7.c rejected
backtest: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins_4h
idea tested: 027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4299 USD
---
## Findings
- **F1:** In coins with a negative prior 30-day return, ordinary drops below the prior 24-hour high are followed by lower than usual returns, not a premium. Over 42 bars, drop deciles 4 to 7 show excess returns of -2.15 % (t -2.70), -3.85 % (t -4.82), -2.10 % (t -2.20) and -3.27 % (t -3.61), with about 184 cases each. Over 84 bars, drop quintiles 1 and 3 show -3.88 % (t -2.96) and -3.64 % (t -2.56).
- **F2:** The loss is not tied to how deep the prior downtrend was. Middle-sized drops (deciles 3 to 7) in falling coins lose over 42 bars in every tercile of the prior 30-day return: -2.08 % (t -2.93, n 321), -2.89 % (t -4.39, n 312) and -2.59 % (t -3.87, n 288).
- **F3:** The forecast's middle tercile carries the rejection. On active bars its mean drop is about 0.95 to 1.0 ranges, and it shows -1.30 % over 18 bars (t -5.51, n 1334) and -2.58 % over 42 bars (t -5.25, n 545). The top tercile, with a mean drop of 2.3 ranges, is near zero at every horizon: +0.01 % over 84 bars (t 0.01). Only the most extreme panics escape the drift down.
- **F4:** In falling coins, only the top drop decile rebounds, and only at a short horizon. It averages 3.75 bar ranges of drop and gives +0.90 % excess over 18 bars (t 2.30, n 444). Over 42 bars this fades to +0.57 % (t 0.59), and the top quintile over 84 bars gives +2.65 % (t 1.50, n 116) with years ranging from -14.7 % (2019) to +10.0 % (2025).
- **F5:** The panic premium appears clearly in coins whose prior 30-day return is positive, over 18 bars (3 days). The top drop decile, with a mean drop of 4.5 ranges, shows +3.18 % excess (t 5.80, n 436). The excess rises from decile 7 (+1.12 %) through decile 8 (+0.79 %) to decile 9.
- **F6:** The 3-day rebound after large drops in rising coins is broad but not in every year. In the top two deciles, 84 % of the 19 coins have a positive mean. It is positive in 2020 (+5.38 %, t 5.78), 2021 (+2.88 %, t 2.08), 2024 (+4.30 %, t 4.30) and 2025 (+3.24 %, t 3.26), and negative in 2022 (-1.21 %, t -1.24) and 2018 (-2.66 %).
- **F7:** The rebound in rising coins does not last to the plan's horizon. The top drop decile shows +2.37 % over 42 bars (t 1.90), and the top quintile shows +0.05 % over 84 bars (t 0.04). The 3-day move of about +3.2 % is still about 14 times the 0.22 % cost of a trade.

## Ideas
- `027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.c1_panic-rebound-in-uptrends` (from F5, F6, F7): In a coin whose 30-day return is positive, a 24-hour stretch in which the close falls far below the stretch's high, measured in the coin's 30-day average 4-hour range, is followed by higher than usual returns over the next 3 days, and the deeper the fall, the higher the return.
- `027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.c2_downtrend-dips-keep-falling` (from F1, F2, F3): In a coin whose 30-day return is negative, the further its close falls below its prior 24-hour high, measured in its 30-day average 4-hour range, the lower its return compared with usual over the next 7 days.
- `027-03_panic-rebound-in-downtrend.b1_downtrend-panic-rebound-more-coins.c3_downtrend-panic-short-rebound` (from F4, F3): In coins whose 30-day return before the panic was negative, a 24-hour stretch with a range several times its 30-day average and a hard fall is still followed by higher than usual returns, only over the next 3 days, and the more extreme the panic, the higher the return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
