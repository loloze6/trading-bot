---
brief: 016_grind-versus-jump-moves
source-idea: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
line: 7.d not profitable
backtest: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 2 to 3 days, the more of its hourly movement over that period went in the direction of the rise (net move relative to the sum of absolute hourly moves), the more it rises over the next 3 days. This holds with the share and the rise read as their averages over the past day, so the smoothness that matters is the one that has persisted for a day rather than its hour-to-hour flicker.
Consequence: A trader should size a 3-day long by how smooth the rise has been across the whole past day and leave it alone through hourly wobbles, instead of re-trading it every hour.
Why:
- F1: Fees, not a wrong forecast, are what sink the book: its gross gain is +0.00054 a day but fees cost 0.00099 a day, leaving the measured mean daily return of -0.00046. Turnover is 0.92 of the book a day, each unit of turnover costs 0.00108, and the book made 55,403 trades with a median length of only 6 hours.
- F2: The position churns far faster than the 3-day effect it bets on. Inside the regime the forecast moves 1.69 points every hour. The rise-over-48-and-72-hours regime lasts only 13.1 hours on average. Regime flips happen on just 6.0% of bars yet carry 41.9% of all turnover.
- F3: A slower book keeps most of the gain and turns the result positive: holding each day's opening position for 24 hours keeps gross at 0.00047 a day (88% of the original). It cuts turnover from 0.92 to 0.21 a day and fees from 0.00100 to 0.00023, giving about +0.00025 a day net. The raw efficiency ratio held daily gives +0.00014 a day against -0.00087 when traded hourly. This is a per-bar estimate, not the book's daily-return measure.
- F4: The forecast carries the graded 3-day information the idea claims. On the non-overlapping 72-hour grid, the top two forecast quartiles earn +0.0050 and +0.0046 excess 72-hour return, against +0.0001 and +0.0008 for the bottom two (about 563 cases each). Active grid bars earn +0.0026 excess (2,254 cases) against -0.0017 when flat (3,429 cases).
