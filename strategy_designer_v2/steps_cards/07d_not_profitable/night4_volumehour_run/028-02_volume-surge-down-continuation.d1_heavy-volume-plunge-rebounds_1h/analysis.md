---
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h
idea tested: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3504 USD
---
## Findings
- **F1:** The book trades far too often on falls that carry no rebound. It held a long position on 65 % of bars and made 24,993 trades, all long, with a median holding of 4 hours. These trades averaged +0.021 % before fees and −0.079 % after. 17,893 of them entered at a forecast above 10 and averaged −0.05 % gross. Standardising over 500 hours and cubing pushes ordinary falls to the top of the forecast range.
- **F2:** The rebound exists only in the extreme tail of the hour's fall times its volume ratio. Over 4 hours (non-overlapping cases), every case below the 90th percentile shows an unusual move near zero: −0.012 %, −0.002 % and −0.006 %, with t between −0.8 and −0.1, over 14,553 cases. Above that the move rises steadily. It is +0.19 % (t 1.47, n 485) for the 95–98th percentile, +0.38 % (t 2.16, n 243) for the 98–99.5th, and +0.79 % (strength 0.49, n 81) above the 99.5th.
- **F3:** Only those tail cases move more than a trade costs. The tested cases' total move is +0.07 % against a cost of 0.11 % (0.6 times). The total 4-hour move is +0.21 % in the 95–98th percentile and +0.40 % in the 98–99.5th. Over 12 hours those percentiles reach +0.49 % and +0.94 %.
- **F4:** Volume decides whether a large fall rebounds. Among hours falling at least 2 of their 30-day standard deviations, the third with the highest volume (8.2 times average) gained +0.54 % over 4 hours (t 2.31, n 274) and +1.34 % over 12 hours (t 1.88). The lowest-volume third (1.5 times average) gained +0.01 % (t −0.09).
- **F5:** The tail effect lives in high-volatility periods. Among the top 5 % of volume-weighted falls, cases in the coin's highest tercile of 30-day hourly volatility gained +0.91 % over 4 hours (t 3.15, n 271) and +2.44 % over 12 hours (t 3.14, n 91). The middle tercile gained −0.05 % (t −0.52) over 4 hours and −1.47 % (t −2.08) over 24 hours. The lowest tercile gained +0.12 % (t 1.02).
- **F6:** The book loses ground to holding in every year. Its mean daily return was below the coins' own in each year from 2018 to 2025. In 2022 it was −0.30 % a day against −0.23 %, and in 2025 −0.19 % against +0.02 %, which leaves the Sharpe at −0.47 against holding's +0.64.

## Ideas
- `028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds.d1_heavy-plunge-rebounds-in-turbulence` (from F2, F4, F5, F3): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rebounds over the next four to twelve hours, and the larger that hour's fall times its volume ratio, the larger the rebound, only while the coin's typical hourly move over the past 30 days is high compared with its own past year.
- `028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds.d2_rarest-plunges-rebound-over-half-day` (from F1, F2, F3, F4): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rebounds over the next twelve hours. The rebound grows steeply with that hour's fall times its volume ratio, measured against the same product over the coin's past year, so that the rarest plunges are followed by rebounds several times larger than those after merely large ones.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
