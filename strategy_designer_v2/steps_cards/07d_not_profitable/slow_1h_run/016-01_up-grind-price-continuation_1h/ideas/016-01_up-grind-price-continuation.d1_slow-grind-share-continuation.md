---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation
line: 7.d not profitable
backtest: 016-01_up-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that rise made by many small hourly gains in the same direction rather than by its few biggest hours, the more the coin keeps rising over the next 3 days, with that share taken as its average over the past day, so that the signal follows the share's slow level rather than its hour-to-hour changes.
Consequence: A trader would hold a grind-sized long through the 3-day horizon instead of resizing it every hour, which keeps the 3-day gain and cuts the fees that consume it.
Why:
- F1: Fees, not the forecast, sink the book: it earns 0.000302 a day before costs but pays 0.000810 a day in fees on a turnover of 0.75 of the book a day, which leaves a mean daily return of -0.000522 and a Sharpe of -1.016.
- F2: The book trades hour by hour while its idea speaks of a 3-day horizon: its 20,233 trades last a median of 300 minutes (mean 892), and each pays a mean commission of 0.31 % against a median gross result of -0.25 %.
- F4: Among those grid cases, a larger grind share comes before a larger 3-day return, though the step flattens above the middle: the next-72-bar return is 0.0081, 0.0145 and 0.0139 across the raw-share thirds (about 313 cases each).
- F5: Inside active hours, the next hour does worse when the grind share is high: the next-hour return by raw-share fifth is 0.00019, 0.00024, 0.00020, -0.00003 and -0.00011, while the forecast is capped at 20 in the top two fifths of forecast, so the position moves with hourly noise that holds no gain.
- F6: The book's timing is negative: of its -0.000522 mean daily return, 0.000156 comes from the market's own rise and -0.000678 from timing. The next-hour return is 0.00023 at 5–23 hours after activation but -0.00002 at 23–71 hours, so the position's hour-to-hour swings miss the move.
