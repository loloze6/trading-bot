---
line: 7.d not profitable
backtest: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d
idea tested: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 0
cost: 0.1904 USD
---
## Findings
- **F1:** The book failed on two measures, both from how seldom it holds a position, not from losing trades: its mean daily return is 0.000333 against the 0.0005 required and it trades 0.00695 times per day against the 0.01 required, while its Sharpe (1.117, 0.551 above holding's), its Sharpe with one window left out (0.741) and its Calmar (0.945) all pass.
- **F2:** The move per case is far larger than a trade costs: each of the 64 upward cloud crosses is followed by a +23.71 % total move over 40 days and a +18.95 % unusual move (0.429 of the coin's usual 30.89 % move), which is 122.9 and 98.2 times the 0.19 % round-trip cost, so costs do not explain the low gain.
- **F3:** The signal is rare because it exists on one bar only: the forecast is non-zero only on the bar of cross age 1, and only when the standardised 60-day return is positive. That gives 64 cases over about 17,400 coin-days (6 coins, 23 to 24 windows, 2,800 to 2,921 bars each), about one bet per coin every 270 days, and leaves the book flat most of the time.
- **F4:** The 60-day return does not grade the move: the slope of the unusual 40-day move on the forecast is 0.0025 with t 0.14 over 64 cases, while the mean unusual move over the same cases is +18.95 %. The gain comes from the cross itself, and setting non-positive 60-day returns to zero removes crosses that carry the same move.
- **F5:** Earlier runs agree that daily continuation moves outlast their horizon and that a book holding each signal for its horizon pays more often when the move per case covers the cost (findings F9 and F11: 6 of 11 held books against 13 of 58 re-sized ones). This points to staying in the move after the cross rather than acting on the cross day alone.

## Ideas
- `021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold.d1_fresh-cloud-breakout-persists` (from F1, F2, F3, F5): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 40 days, and the larger the coin's 60-day return before the cross, the larger the rise; this holds on every day of the following 20 days on which the close is still above the cloud, and the more recent the cross, the larger the rise.
- `021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold.d2_thin-cloud-breakout-strength` (from F2, F3, F4): After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 40 days, and the thinner the cloud at the cross, measured as its width relative to the close, the larger the rise.
- `021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold.d3_above-rising-cloud-trend` (from F1, F3, F5): While a coin's daily close stays above its Ichimoku cloud, the coin rises over the next 40 days, and the steeper the cloud's rise over the past 26 days, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
