---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a 24-hour fall that is large against the coin's usual 24-hour move, while its bar range over those 24 hours is above its 30-day average, the coin earns more than its usual drift over the next 14 days, only while its price is below its 90-day average. The further the price is below that average, and the larger the fall times the range expansion, the larger that excess.
Consequence: A trader would buy panic sell-offs only in coins already trading at a deep discount to their 90-day average, and stay out of panics near or above it, where the book's deepest losses came.
Why:
- F2: The panic effect the book bets on has no size. The unusual move is +0.05 % per case over 14 days, strength −0.008, t 0.09 over 1050 cases, with a negative slope (−0.0008). On the 84-bar grid, no severity quintile of fall × range ratio reaches t 1.5; the largest is +3.98 % with t 1.45 over 31 cases. So the +2.14 % total move per case is almost entirely the coins' drift.
- F3: The book's losses sit where price is near its 90-day mean, and its worst days come with heavier positions in coins above that mean.
- F4: Coins far below their 90-day mean earn an excess over 14 days; coins near it do worse than drift.
