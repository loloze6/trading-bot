---
line: 7.g patterns
backtest: 067-02.b1.b1_choppy-deep-month-fall-continues_1d
idea tested: 067-02.b1.b1_choppy-deep-month-fall-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4607 USD
---
## Findings
- **F1:** In a choppy market, a coin with high agitation (its 30-day swing above its own median) fell over the next 7 days after a month down and also after a month up. After a month down the drift-adjusted 7-day return was -8.66 % (41 cases on 26 days, day-clustered t -3.07). After a month up it was -5.65 % (16 cases on 15 days, t -2.08). In a calm choppy market the two sides split instead: -3.07 % after a fall (t -1.65) and +3.03 % after a rise (t 1.31), and neither can be told from 0.
- **F2:** Inside the choppy agitated market the decline grows as the 30-day return gets lower. By quartile of that return, the next 7 days run -11.87 %, -9.16 %, -4.41 % and -5.54 % (about 14 to 15 cases each, t -3.25, -3.48, -2.46, -1.74). Across all choppy bars the 30-day return quintiles show the same order, from -9.39 % (t -4.95) up to +1.82 %.
- **F3:** The book's gain comes almost entirely from choppy agitated falls. Its position gain over 7 bars was +2.10 % there (41 cases, t 2.82). It was +0.49 % in calm falls (70 cases, t 0.49) and slightly negative on rises. The calm choppy cases, the larger group, dilute an effect of about 8 % to a book mean of 0.011 % a day on days in a position.
- **F4:** The choppy agitated decline repeats in 3 of 4 years: 2018 -10.9 %, 2020 -13.6 %, 2021 -9.0 % (t -2.26, -2.98, -5.19). In 2019 it was -0.6 % (t -0.37). It is negative in 9 of the 10 windows that hold cases, and it does not depend on how far the swing sits above its median (terciles -7.5 %, -7.8 %, -8.2 %).
- **F5:** In trending agitated markets (rising or falling), a day that closes in the top fifth of its range is followed by a 7-day excess return of +7.74 %. A day closing in the bottom fifth is followed by -2.02 % (Welch t 4.49, 546 cases). The top-minus-bottom gap over all bars is positive in every year: 2018 +3.5 %, 2019 +5.1 %, 2020 +5.5 %, 2021 +9.1 % (t 1.17 to 3.66).
- **F6:** Where the close sits in its 7-day range sorts the next week in order. By quintile the next 7 days run -2.33 %, -0.94 %, +0.22 %, +0.15 % and +1.76 %; the bottom quintile has t -2.60 on 89 days and the top t 1.76 on 96 days.
- **F7:** The tested short's total move per case is -0.01 % against a trade cost of 0.22 %. The coins' upward drift cancels its +1.13 % unusual move. In the choppy agitated cells, the 5.7 to 8.7 % excess decline is many times that cost.

## Ideas
- `067-02.b1.b1.g1_choppy-agitated-month-weakness-falls` (from F1, F2, F3, F4, F7): In a choppy, agitated market, the lower a coin's return over the past 30 days, the more it falls over the next 7 days. The deepest monthly falls are followed by the largest weekly declines, and even modest monthly rises are followed by declines.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `067-02.b1.b1.g2_agitated-high-close-continues` (from F5, F6): In an agitated market, the higher a coin's daily close sits within that day's high-to-low range, the more the coin rises over the next 7 days. Closes at the very top are followed by the largest gains and closes at the bottom by further falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
