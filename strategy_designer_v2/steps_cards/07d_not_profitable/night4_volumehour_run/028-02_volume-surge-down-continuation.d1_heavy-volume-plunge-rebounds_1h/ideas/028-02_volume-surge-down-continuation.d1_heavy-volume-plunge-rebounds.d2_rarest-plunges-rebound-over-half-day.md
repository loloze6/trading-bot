---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rebounds over the next twelve hours. The rebound grows steeply with that hour's fall times its volume ratio, measured against the same product over the coin's past year, so that the rarest plunges are followed by rebounds several times larger than those after merely large ones.
Consequence: Only the rarest heavy-volume plunges are worth buying, held for about half a day, while ordinary large falls are a reason to stay out.
Why:
- F1: The book trades far too often on falls that carry no rebound. It held a long position on 65 % of bars and made 24,993 trades, all long, with a median holding of 4 hours. These trades averaged +0.021 % before fees and −0.079 % after. 17,893 of them entered at a forecast above 10 and averaged −0.05 % gross. Standardising over 500 hours and cubing pushes ordinary falls to the top of the forecast range.
- F2: The rebound exists only in the extreme tail of the hour's fall times its volume ratio. Over 4 hours (non-overlapping cases), every case below the 90th percentile shows an unusual move near zero: −0.012 %, −0.002 % and −0.006 %, with t between −0.8 and −0.1, over 14,553 cases. Above that the move rises steadily. It is +0.19 % (t 1.47, n 485) for the 95–98th percentile, +0.38 % (t 2.16, n 243) for the 98–99.5th, and +0.79 % (strength 0.49, n 81) above the 99.5th.
- F3: Only those tail cases move more than a trade costs. The tested cases' total move is +0.07 % against a cost of 0.11 % (0.6 times). The total 4-hour move is +0.21 % in the 95–98th percentile and +0.40 % in the 98–99.5th. Over 12 hours those percentiles reach +0.49 % and +0.94 %.
- F4: Volume decides whether a large fall rebounds. Among hours falling at least 2 of their 30-day standard deviations, the third with the highest volume (8.2 times average) gained +0.54 % over 4 hours (t 2.31, n 274) and +1.34 % over 12 hours (t 1.88). The lowest-volume third (1.5 times average) gained +0.01 % (t −0.09).
