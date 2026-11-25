---
line: 7.g patterns
backtest: 037-01_agitated-ordinary-rise-next-day-giveback_1d
idea tested: 037-01_agitated-ordinary-rise-next-day-giveback
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3991 USD
---
## Findings
- **F1:** In agitated markets, the lower a coin closes within its day's high-low range, the higher its next-day return over its drift. The slope on (0.5 − close position) is +1.86 % (t 2.99, cases of one day together, 3,691 bars). In calm markets it is only +0.63 % (t 1.47, 4,639 bars).
- **F2:** The close-location effect in agitated markets carries more than the tested idea's own signal. With both in one regression on agitated bars, the coefficient on (0.5 − close position) is +1.05 % against −0.33 % for the volatility-scaled return (2,946 bars). In calm bars the two are +0.22 % and −0.14 % (4,005 bars).
- **F3:** The agitated close-location slope is positive on every coin and in every year shown.
- **F4:** Across all agitated days, the next-day excess return falls steadily as the close moves up the range.
- **F5:** The tested signal points the same way on all six coins: an agitated ordinary rise (scaled rise 0 to 1) is followed by a next-day excess return of −0.30 % (XRP) to −1.12 % (ZEC, t −2.76). Only ZEC reaches |t| 2; the other five have t from −0.49 to −1.63.
- **F6:** The book does not convert that edge into profit.
- **F7:** The next-day reversal does not carry into a longer horizon in a way that can be told from chance.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `037-01.g1_agitated-close-location-reversal` (from F1, F2, F3, F4, F6): In an agitated market, the lower a coin closes within its day's high-low range, the higher its return over the next day; closes near the day's high are followed by the weakest next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
