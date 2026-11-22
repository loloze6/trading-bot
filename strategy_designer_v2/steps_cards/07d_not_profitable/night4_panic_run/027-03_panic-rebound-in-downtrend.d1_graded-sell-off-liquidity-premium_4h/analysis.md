---
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
idea tested: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3872 USD
---
## Findings
- **F1:** The book is a near-permanent long and its falls are the coins' falls. It holds a position on 85 % to 97 % of bars in every prior-30-day-return quintile, with mean allocation 0.74 to 1.09, and the median trade lasts 30.7 days. Its window sums track holding: w2 −0.51 against −0.46, w14 −0.65 against −0.52, w7 −0.34 against −0.58. The chained book's deepest fall is −74.2 % against a yearly return of 27.2 %, hence Calmar 0.37.
- **F2:** The panic effect the book bets on has no size. The unusual move is +0.05 % per case over 14 days, strength −0.008, t 0.09 over 1050 cases, with a negative slope (−0.0008). On the 84-bar grid, no severity quintile of fall × range ratio reaches t 1.5; the largest is +3.98 % with t 1.45 over 31 cases. So the +2.14 % total move per case is almost entirely the coins' drift.
- **F3:** The book's losses sit where price is near its 90-day mean, and its worst days come with heavier positions in coins above that mean.
- **F4:** Coins far below their 90-day mean earn an excess over 14 days; coins near it do worse than drift.
- **F5:** The book loses in calm stretches it holds through. With the 24-hour range ratio in its lowest quintile (0.16 to 0.62), the book makes −0.204 % a day against the coin's +0.058 %. In the highest quintile (above 1.23), it makes +0.287 % against the coin's +0.245 %.
- **F6:** The gain is uneven across coins. ZEC trades average +34.5 % net, against +1.4 % to +9.5 % for the other five coins.

## Ideas
- `027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium.d1_panic-rebound-below-90-day-mean` (from F2, F3, F4): After a 24-hour fall that is large against the coin's usual 24-hour move, while its bar range over those 24 hours is above its 30-day average, the coin earns more than its usual drift over the next 14 days, only while its price is below its 90-day average. The further the price is below that average, and the larger the fall times the range expansion, the larger that excess.
- `027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium.d2_deep-discount-90-day-reversal` (from F3, F4): The further a coin's price stands below its 90-day average, the more it earns above its usual drift over the next 14 days.
- `027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium.d3_panic-premium-during-wide-ranges` (from F1, F5): After a 24-hour fall that is large against the coin's usual 24-hour move, while its bar range over those 24 hours is above its 30-day average, the coin earns more than its usual drift over the next 14 days, only while its 24-hour range stays above its 30-day average. The wider that range against its average, the larger that excess.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
