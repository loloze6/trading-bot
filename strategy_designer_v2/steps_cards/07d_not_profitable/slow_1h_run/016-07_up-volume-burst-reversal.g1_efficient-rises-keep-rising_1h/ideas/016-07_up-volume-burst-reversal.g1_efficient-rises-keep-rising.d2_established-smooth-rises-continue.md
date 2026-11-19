---
brief: 016_grind-versus-jump-moves
source-idea: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
line: 7.d not profitable
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 2 to 3 days, the more of its hourly movement over that period went in the direction of the rise (net move relative to the sum of absolute hourly moves), the more it rises over the next 3 days, only while its 3-day return has stayed positive at every close over the past day.
Consequence: A trader should join a smooth rise only once it has held its gain for a full day, sized by its smoothness, and not chase rises that just tipped positive and flip back within hours.
Why:
- F2: The position churns far faster than the 3-day effect it bets on. Inside the regime the forecast moves 1.69 points every hour. The rise-over-48-and-72-hours regime lasts only 13.1 hours on average. Regime flips happen on just 6.0% of bars yet carry 41.9% of all turnover.
- F4: The forecast carries the graded 3-day information the idea claims. On the non-overlapping 72-hour grid, the top two forecast quartiles earn +0.0050 and +0.0046 excess 72-hour return, against +0.0001 and +0.0008 for the bottom two (about 563 cases each). Active grid bars earn +0.0026 excess (2,254 cases) against -0.0017 when flat (3,429 cases).
- F5: Even before fees, most of the gain comes from the market's own rise rather than timing. The market part is 1.35e-5 per bar and timing 0.89e-5 per bar. The book is long only 45% of bars, so it earns -0.00046 a day while the coins' own mean is +0.00119 a day.
