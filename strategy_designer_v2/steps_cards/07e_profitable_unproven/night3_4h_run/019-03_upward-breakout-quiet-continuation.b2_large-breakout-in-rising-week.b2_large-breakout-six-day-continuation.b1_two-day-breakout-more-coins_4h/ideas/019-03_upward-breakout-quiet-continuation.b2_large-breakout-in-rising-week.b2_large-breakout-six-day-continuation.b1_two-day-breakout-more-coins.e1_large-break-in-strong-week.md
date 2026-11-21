---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's four-hour close breaks above the highest high of its preceding two days, the farther the close sits above that high (in the coin's 30-day average four-hour range) and the stronger the coin's 7-day return, the larger the coin's rise over the next six days.
Consequence: A trader would buy only the large breaks made in a strongly rising week and refuse the marginal ones, which follow with no move above the coin's drift.
Why:
- F1: The idea's grading is there, but the test could not see it. The forecast sits at its cap of 20 on at least 75 % of entries (median 20, mean 18.77), so the median split left 0 cases in the larger half. Graded by the raw break instead (close minus the two-day high, in 30-day average 4h ranges), the 6-day unusual move rises from -0.53 % in the smallest quintile (break 0.07 ranges) to +2.88 % in the largest (break 1.52 ranges). Strength goes from -0.043 to +0.187, about 680 cases per quintile.
- F2: The largest-break quintile's unusual move of +2.88 % per case is about 13 times the 0.22 % round-trip cost. The two smallest quintiles are at or below zero (-0.53 %, -0.03 %), so most of the book's bets carry no move of their own.
- F4: The 7-day return grades the move too. Among breaks, the top quintile of 7-day return (median +21 %) is followed by +3.66 % unusual move over 6 days (strength 0.22). The lower four quintiles range from -0.64 % to +1.00 %.
- F5: Break size and 7-day return add up. The largest-break third combined with the strongest-week third gives +3.50 % over 6 days (505 cases). The smallest-break third gives -0.07 % to -0.48 % at any 7-day return.
- F9: The grading holds coin by coin. In 15 of 19 coins, the largest-break third beats the smallest over 6 days (per-coin rank correlations up to 0.27).
- F10: The horizon fits. The bets' unusual move has t 1.33 at 1 day, 2.40 at 2 days, 2.85 at 6 days and 1.67 at 12 days.
