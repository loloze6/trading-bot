---
line: 7.g patterns
backtest: 067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues_1d
idea tested: 067-01.b1.g1.b1.d1_choppy-deep-month-slide-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4237 USD
---
## Findings
- **F1:** In the choppy regime (60-day return between -10 % and +10 %), the coin's 10-day unusual move falls with its 30-day return across quintiles. The deepest-fall quintile (mean 30-day return -25.3 %) is followed by -12.8 % (t -4.22, 32 cases on 18 days). The next quintile gives -4.4 % (t -1.52), and the middle quintiles give +2.9 % and +0.4 %.
- **F2:** Among choppy-regime falls only, the continuation grows with the depth of the 30-day fall. Signed continuation by tercile of fall size is -3.7 % (t -1.15), +5.9 % (t 1.82) and +13.8 % (t 4.58, 28 cases, 16 days). The effect is steep and carried by the deepest slides.
- **F3:** Within the deepest 30-day-fall tercile in chop, a slide whose last 5 days also fell most is followed by a 10-day unusual move of -17.1 % (t -5.17, 27 cases, 12 days). Slides whose last 5 days were flat or up give -5.1 % (t -2.11) and -5.6 % (t -1.64).
- **F4:** The continuation after 30-day falls in chop lives where the coin is agitated (30-day swing above its median). Agitated falls continue by +9.2 % (t 2.86, 33 cases, 18 days); calm falls continue by +2.8 % (t 0.80, 50 cases).
- **F5:** The deepest-fall quintile continues at every horizon tested. It gives -7.5 % over 5 days (t -2.76, 62 cases, 38 days), -12.8 % over 10 days and -18.1 % over 20 days (t -5.91, but only 8 days).
- **F6:** The rise side shows no reliable continuation. In the top 30-day-return quintile in chop, the mean is +12.3 % with t 1.24, and the median is only +2.5 %. Signed continuation is +2.2 % (t 0.32) in agitated rises and +5.9 % (t 0.99) in calm rises.
- **F7:** Outside chop, the 30-day return orders nothing. In falling and rising markets the tercile means are between -3.1 % and +5.5 %, all with |t| < 1.5.
- **F8:** The book does not capture the bar-level effect, and the gap is in the strategy rather than in the effect. Its trades lose after fees in every forecast tercile (mean -3.05 %, -1.21 %, -3.12 %; win rates 32 %, 40 %, 44 %; 424 trades, median 10 days). Yet the raw deepest-slide cases move about 13 % their way over 10 days, which suggests the forecast standardised over its own 60 values does not point at the raw deep slides of F1 and F2.

## Ideas
- `067-01.b1.g1.b1.d1.g1_agitated-chop-slide-continues` (from F4, F2, F1): In a choppy, agitated market, the larger a coin's percentage fall over the past 30 days, the more it keeps falling over the next 10 days.
- `067-01.b1.g1.b1.d1.g2_accelerating-month-slide-continues` (from F3, F2): In a choppy market, among coins that fell over the past 30 days, the larger the fall over the last 5 days on top of the month's slide, the more the coin keeps falling over the next 10 days.
- `067-01.b1.g1.b1.d1.g3_chop-slide-twenty-day-continuation` (from F5, F1, F2): In a choppy market, the larger a coin's percentage fall over the past 30 days, the more it keeps falling over the next 20 days, the continuation growing with the depth of the slide.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
