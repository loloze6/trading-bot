---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours after 21:00 UTC, and the larger its fall over the past 24 hours measured in units of its 7-day hourly volatility, the larger that rise, with the rise concentrated in the first hour after 21:00 UTC.
Consequence: A trader would keep only the first hour of the evening rebound, the hour that carries the gain, and would stop paying for a second hour that loses.
Why:
- F1: Fees remove the whole gain: the book earns 1.30e-5 per bar before fees but pays 2.10e-5 per bar in fees, so the 10,709 trades (all long) average +0.083% before fees and -0.017% after, about 0.10% of cost per round trip.
- F7: The second hour of the hold loses money: trades held at most 60 minutes average +0.28% before fees (n 3,926), while trades held 60 to 120 minutes average -0.06% (n 6,451); the hour-22 bars carry 2.2e-4 of fees per bar against a gain of -1.3e-6.
- F5: The raw volatility-scaled 24-hour fall is graded where the standardised forecast is not: among falls, the two deepest quintiles (mean z -1.71 and -0.86) give excess 2-hour returns of +0.0019 and +0.0022, against +0.0003 to +0.0012 for the shallower three.
