---
line: 7.b inconclusive
backtest: 054-01_deep-reclaimed-low-pierce-rebound_1d
idea tested: 054-01_deep-reclaimed-low-pierce-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2907 USD
---
## Findings
- **F1:** In folds B and C, reclaimed 30-day-low pierces inside the falling agitated profile were followed by a 5-day unusual move of +4.7 %. That rests on 26 cases on 15 days, with t 1.45. The move was +2.8 % over 3 days (t 1.01) and +5.7 % over 10 days (t 1.13). The median was +3.9 %, 67 % of cases were positive, and the mean strength was 0.45 of a usual move. The effect is on the predicted side, but there are too few cases to clear the bar.
- **F2:** Step 5's main measure over all folds is on the predicted side but short of the bar: +1.59 % per case (t 0.92) over 5 days, from 75 cases on only 50 days. The total move of +2.23 % is 11.6 times the 0.19 % cost of a trade, so the size is not the limit; the small number of independent days is.
- **F3:** The same reclaims outside the profile fell instead. Over 5 days they averaged -4.1 % (112 cases on 74 days, t -1.95), and over 10 days -5.6 % (t -2.84). The rebound lives only inside the named profile.
- **F4:** A falling trend alone is not enough. Reclaims in any falling market, agitated or not, averaged +0.2 % over 5 days (70 cases, t 0.10). In markets that were not falling they averaged -5.2 % (68 cases, t -1.74). The agitation half of the profile carries the effect.
- **F5:** Inside the profile the rebound is broad across coins: 5 of 6 coins were positive (XMR +13.4 %, BTC +5.1 %, ETH +3.8 %, ZEC +1.2 %, LTC too few cases, XRP -1.1 %). It was also positive in both years with enough cases (2018 +5.8 % on 8 days, 2021 +8.9 % on 2 days). No single coin or year accounts for it.
- **F6:** Inside the profile in folds B and C, the depth grading did not show:

## Ideas
- `054-01.b1_reclaimed-low-all-coins` (from F1, F2, F5): In a falling, agitated market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it rises over the next 5 days, and the rise is larger the deeper the day's low went below the 30-day low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
