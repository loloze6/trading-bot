---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the 24 hours after 21:00 UTC, and the larger its fall over the past 24 hours measured in units of its 7-day hourly volatility (the raw scaled fall, not that fall ranked against its own recent values), the larger that rise.
Consequence: A trader would hold the evening rebound for a day instead of two hours, so that a move several times one round-trip cost pays for a single fee, and would size it by the raw volatility-scaled fall.
Why:
- F1: Fees remove the whole gain: the book earns 1.30e-5 per bar before fees but pays 2.10e-5 per bar in fees, so the 10,709 trades (all long) average +0.083% before fees and -0.017% after, about 0.10% of cost per round trip.
- F3: The two-hour forward move the book trades is about the size of one round-trip fee: on 20:00 UTC bars with forecast > 0 the excess 2-hour return is +0.0006 to +0.0018 by forecast quintile (t 7.39, n 8,613), against roughly 0.0010 of fees per trade.
- F5: The raw volatility-scaled 24-hour fall is graded where the standardised forecast is not: among falls, the two deepest quintiles (mean z -1.71 and -0.86) give excess 2-hour returns of +0.0019 and +0.0022, against +0.0003 to +0.0012 for the shallower three.
- F6: After the deepest raw falls the rise carries on over a full day and grows past the fee: the excess 24-hour return is +0.0018 and +0.0026 for the two deepest z quintiles, against -0.0001, -0.0010 and -0.0017 for the shallower three (n about 1,630 each).
