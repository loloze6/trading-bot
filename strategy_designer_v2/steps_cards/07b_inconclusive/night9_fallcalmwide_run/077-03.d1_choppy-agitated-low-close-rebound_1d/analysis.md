---
line: 7.b inconclusive
backtest: 077-03.d1_choppy-agitated-low-close-rebound_1d
idea tested: 077-03.d1_choppy-agitated-low-close-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3724 USD
---
## Findings
- **F1:** The tested forecast misses where the effect is. In the profile (folds B and C), low closes fall into five quintiles of the raw product (the close's distance below the middle times the day's range in 30-day swings). The next-day excess return is flat or negative in the three weaker quintiles: +0.18 %, −0.42 % and −1.21 %, with t between −1.3 and 0.3 (about 32 cases each). It turns positive only in the two strongest: +2.09 % (t 1.66) and +2.36 % (t 1.90). The step-5 forecast, standardised over its past 60 values, mixes these together, which gives a weighted mean of +0.34 % with t 1.19.
- **F2:** The strongest 40 % of low closes give a next-day excess return of +2.22 %, with t 2.32 when the cases of one day are taken together (65 cases, 46 days). The other 60 % give −0.50 % (t −0.83, 96 cases). The least-squares slope of the next-day return on the raw product is 0.0197 (p 0.0004). The rise is graded, but it shows only on the widest, lowest closes.
- **F3:** These strongest low closes rise on most coins and in every year. By coin: XMR +3.40 % (t 2.91, 14 cases), ZEC +4.54 % (t 1.81, 14), BTC +0.86 %, ETH +1.72 % and XRP +4.86 %. LINK (−1.75 %, 8 cases) and LTC (−0.90 %, 4) go the other way. By year the mean is positive throughout: 2018 +6.98 %, 2019 +2.41 % (t 2.52), 2020 +3.30 % and 2021 +0.68 %.
- **F4:** The tested book is too small to cover its costs. Its total move per case is +0.17 % against a 0.22 % trade cost, and its unusual move is +0.03 % (t 0.15). The strongest low closes move about +2.2 % in a day, about ten times the cost.
- **F5:** High closes in the profile are followed by a fall, but not clearly. The next-day excess return is −1.04 % (t −1.72, 196 cases), and −1.29 % (t −1.37) on the strongest 40 %. Fading both sides together gives +0.84 % (t 1.26). The long side alone carries the clearer graded effect.
- **F6:** Outside the profile, the strongest quintile of low closes also rises the next day: +1.03 %, t 4.86, 729 cases over 246 days. This is a wider profile than the brief names, so it is a discovery off this theme and not a follow-up of it.

## Ideas
- `077-03.d1.b1_widest-low-close-next-day-rebound` (from F1, F2, F3, F4): In a choppy, agitated market, a day that closes near its low on a range wide against the coin's 30-day swing is followed by a rise over the next day. The rise is larger the wider the day against that swing and the nearer the close sits to the low, and it shows on the widest, lowest closes rather than on mildly low ones.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
