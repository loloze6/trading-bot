---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium
line: 7.g patterns
backtest: 027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After a wide-range 24-hour fall, the coin's excess return over the next 3 days is larger the higher its 30-day return before the fall.
Consequence: A trader would lean hardest into panic sell-offs that hit coins in an uptrend, and take smaller rebound bets in coins already falling.
Why:
- F1: The premium after a wide-range fall is real but short: among non-overlapping 3-day cases, a 24-hour fall of more than one usual 24-hour move with the 24-hour bar range above 1.3 times its 30-day average is followed by an excess of +2.37 % over the coin's 3-day drift (t 4.53, n 299), against +0.66 % (t 1.84, n 480) for the same falls without a wide range. At 14 days the same cases show +2.53 % with t 0.96 (n 48), so the 14-day horizon the idea was tested on dilutes the move into noise.
- F5: The rebound is larger in coins that were rising before the fall. Wide-range falls with a positive 30-day return are followed by +3.95 % over 3 days (t 4.80, n 137), against +1.04 % (t 1.59, n 162) when the 30-day return was negative. This contradicts the brief's "whatever its trend before" in degree, not in sign.
