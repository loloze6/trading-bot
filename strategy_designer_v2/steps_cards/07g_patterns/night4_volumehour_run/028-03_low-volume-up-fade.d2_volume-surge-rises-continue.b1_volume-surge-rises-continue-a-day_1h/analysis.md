---
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day_1h
idea tested: 028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4040 USD
---
## Findings
- **F1:** Over the two hours that start at 20:00 and 21:00 UTC, the coin rises more than usual. The mean strength of the next hour is 0.051 of the usual hourly move for BTC (t 3.81, 5837 hours) and 0.052 for ETH (t 3.92, 5837 hours). It is positive in 7 of 8 years (2022: −0.037, t −1.42) and in every weekday (0.041 to 0.065). The raw mean is +0.042 % an hour for BTC and +0.055 % for ETH. This was 2 of the 24 hours examined, and a t near 4 still stands out after that many looks.
- **F2:** Hourly falls of more than 1.5 of the usual hourly move are followed by a 2-hour rebound that grows with the hour's volume against its 30-day mean. By volume-ratio quartile the mean 2-hour strength is −0.009, 0.076, 0.081 and 0.246 (t −0.20, 1.52, 1.28, 3.34; about 742 cases each). This is uneven by year: with volume above 3 times its mean, it is 0.740 in 2020 (t 3.86) and 0.942 in 2021 (t 3.44), but −0.032 in 2019 and −0.088 in 2025.
- **F3:** In the event grid, falls of −1.5 to −2.5 usual moves on volume above 3 times its mean are followed by a strength of 0.188 over 2 hours (t 2.87, 723 cases) and 0.153 over 6 hours (t 2.30, 466 cases). The same falls on volume under 1.5 times its mean give 0.047 (t 1.53) and 0.054 (t 1.75), so the effect sits on the high-volume falls.
- **F4:** The tested idea's own situation shows no further rise over 24 hours. Rises above 4 usual moves on volume above 3 times its mean give a 24-hour strength of 0.035 (t 0.39, 120 cases). Forecasts above 10 give −0.010 (t −0.14, 261 cases).
- **F5:** The book is mostly the coin held long. It is in a position on 87 % of bars, at a mean allocation of 0.89. Its worst decile of days averages −6.14 % against the coin's −5.67 %, and its best +7.02 % against +7.26 %... more exactly, the coin's +6.57 %. This is why its Sharpe falls 0.058 short of holding.
- **F6:** The hours 00:00 to 02:00 UTC fall more than usual overall: strength −0.030 for BTC (t −3.03) and −0.031 for ETH (t −3.06). This has faded, with 2023 to 2025 at −0.015, +0.0005 and +0.015, so it does not stand out as lasting.

## Ideas
- `028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day.g1_volume-surge-falls-rebound-briefly` (from F2, F3, F4): A coin's hourly fall far larger than its usual hourly move over the past 30 days, on volume above its 30-day average hourly volume, is followed by a rise over the next two hours. The higher that hour's volume against its 30-day average, the larger the rebound.
- `028-03_low-volume-up-fade.d2_volume-surge-rises-continue.b1_volume-surge-rises-continue-a-day.g2_late-us-session-drift` (from F1): A coin rises more than its usual drift over the hours from 20:00 to 22:00 UTC. The rise is about a twentieth of its usual hourly move, so it is larger in percent the higher the coin's hourly volatility over the past 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
