---
line: 7.g patterns
backtest: 058-01.g1_thin-volume-deep-fall-continues_1d
idea tested: 058-01.g1_thin-volume-deep-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4153 USD
---
## Findings
- **F1:** After a day that fell more than 1.5 of the coin's usual daily moves, the next day's excess return grows with that day's volume against its 30-day average, and the volume adds to the fall's own size. On down days beyond 1 usual move (680 cases), the slope of the next-day excess return on the log volume surprise is +0.0122 (t 3.55). The slope on fall size × volume surprise is +0.0048 (t 5.12). The heaviest-volume third of these falls was followed by +2.82 % (t 4.29, 112 cases); the other two thirds by +0.36 % and +0.07 % (t 0.74 and 0.16).
- **F2:** The heavy-volume rebound is not one cluster of days. With the cases of one day taken together it is +6.07 % per day (t 2.24, 52 days). It is positive in every year: 2018 +1.81 %, 2019 +3.50 %, 2020 +5.65 %, 2021 +0.69 %. It is positive on all six coins: BTC +2.58 %, ETH +3.09 %, LTC +4.16 %, XRP +6.93 %, XMR +0.44 %, ZEC +0.42 %.
- **F3:** The heavy-volume rebound lives outside the falling calm profile. Outside it, heavy-volume sharp falls were followed by +3.76 % (t 4.58, 76 cases), against +0.61 % (t 1.38, 143) on lighter volume. Inside falling calm it was only +0.84 % (t 0.82, 36), against −0.47 % (t −1.03, 83) on lighter volume. By trend alone, falling markets gave +3.22 % (t 2.71, 48) on heavy volume and −0.18 % (t −0.34, 77) on light volume. This matches the brief's claim that heavy-volume falls do not carry on, but the effect shows outside the calm downtrend, not inside it.
- **F4:** Inside falling calm, the tested grading is weak. The 5-day excess return by 30-day-return quartile is not monotone: −1.08 %, −2.72 %, +0.30 %, −0.66 % (t at most 2.49, 64 cases each). By volume-shrink tercile it runs −0.43 %, −1.57 %, −2.20 % (thin last, t −1.49). This matches step 5's slope t of 1.22 on 444 cells.
- **F5:** Shallow forecasts lost money in the book. Trades in the tercile with the smallest short forecast lost 1.62 % on average (median −2.82 %, 169 trades). The two deeper terciles made +0.81 % and +0.89 % (175 and 171 trades). Two coins carried the loss: ZEC −3.58 % per trade over 92 trades, and XRP −1.86 % over 70.
- **F6:** A low close is followed by a next-day rise. Bars closing in the lowest fifth of their range were followed by +0.51 % next-day excess return (t 3.74, 1,588 bars), and the highest fifth by −0.40 % (t −2.92). This repeats the held low-close rebound ideas (045-01, 039-02), so it is already held and not a discovery.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `058-01.g1.g1_heavy-volume-fall-rebounds` (from F1, F2, F3): The deeper a coin's one-day fall, measured in its usual daily moves, and the heavier that day's volume against its average of the past 30 days, the more the coin rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
