---
line: 7.b inconclusive
backtest: 041-01_agitated-scaled-rise-next-day-continues_1d
idea tested: 041-01_agitated-scaled-rise-next-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3352 USD
---
## Findings
- **F1:** The tested measure is on the side opposite to the idea: across all agitated up days in folds B and C, the next-day excess return is negative on every coin. It runs from -0.18 % for XRP (t -0.33) to -0.83 % for ZEC (t -2.19). It is negative in 9 of 12 windows, which matches step 5's -0.19 % weighted (t -1.11) and its size of -0.36 % per case (t -2.12).
- **F2:** The 60-day trend splits the effect into two opposite halves, and they cancel. In a rising trend (60-day return above +10 %), agitated up days are followed by +0.25 % excess (396 cases, 178 days, t 1.87). In a falling trend they are followed by -1.05 % (361 cases, 126 days, t -2.69), and in a choppy trend by -1.62 % (59 cases, t -2.14).
- **F3:** In a rising agitated market the continuation grows with the scaled rise. The next-day excess is +0.13 %, +0.22 %, +0.35 % and +0.73 % for scaled rises in (0, 0.5], (0.5, 1], (1, 2] and above 2, though each bin's t is at most 1.08. The correlation of scaled rise with next-day excess is 0.087. The forecast-weighted mean is +0.43 % (t 0.79), and the sign holds on 4 of 6 coins.
- **F4:** In a falling agitated market a scaled rise is given back the next day. The weighted mean is -1.17 % (t -1.88). On the 30-day trend the same split gives -1.15 % (466 cases, 166 days, t -3.08). The grading is uneven: -0.66 %, -2.13 %, -0.46 % and -2.85 % across the four bins of scaled rise.
- **F5:** The trend split is not peculiar to agitated markets. Calm up days show the same pattern: +0.41 % in a rising trend (t 1.12) and -0.35 % in a falling trend (t -1.37). The trend, more than the agitation, sets which way a scaled rise goes next.
- **F6:** The size cannot pay as tested. The total move is -0.23 % per case against a 0.19 % cost per trade. Even the rising-trend half (+0.25 %, F2) only barely covers the cost before drift is removed.

## Ideas
- `041-01.b1_rising-agitated-rise-continues` (from F2, F3, F5): In a rising, agitated market, the larger a coin's one-day rise measured against the standard deviation of its daily returns over the last 30 days, the larger its rise over the next day.
- `041-01.b2_falling-agitated-rise-given-back` (from F2, F4): In a falling, agitated market, the larger a coin's one-day rise measured against the standard deviation of its daily returns over the last 30 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
