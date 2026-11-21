---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold
line: 7.d not profitable
backtest: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 40 days, and the thinner the cloud at the cross, measured as its width relative to the close, the larger the rise.
Consequence: A trader would take every upward cloud breakout, whatever the prior two-month return, and lean harder on those through a thin cloud.
Why:
- F2: The move per case is far larger than a trade costs: each of the 64 upward cloud crosses is followed by a +23.71 % total move over 40 days and a +18.95 % unusual move (0.429 of the coin's usual 30.89 % move), which is 122.9 and 98.2 times the 0.19 % round-trip cost, so costs do not explain the low gain.
- F3: The signal is rare because it exists on one bar only: the forecast is non-zero only on the bar of cross age 1, and only when the standardised 60-day return is positive. That gives 64 cases over about 17,400 coin-days (6 coins, 23 to 24 windows, 2,800 to 2,921 bars each), about one bet per coin every 270 days, and leaves the book flat most of the time.
- F4: The 60-day return does not grade the move: the slope of the unusual 40-day move on the forecast is 0.0025 with t 0.14 over 64 cases, while the mean unusual move over the same cases is +18.95 %. The gain comes from the cross itself, and setting non-positive 60-day returns to zero removes crosses that carry the same move.
