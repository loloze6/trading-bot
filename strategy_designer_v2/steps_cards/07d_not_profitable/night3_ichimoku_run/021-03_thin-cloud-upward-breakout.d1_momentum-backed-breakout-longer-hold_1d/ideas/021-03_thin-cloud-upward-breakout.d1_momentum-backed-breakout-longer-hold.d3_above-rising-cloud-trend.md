---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold
line: 7.d not profitable
backtest: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's daily close stays above its Ichimoku cloud, the coin rises over the next 40 days, and the steeper the cloud's rise over the past 26 days, the larger the rise.
Consequence: A trader would hold a long position for as long as the coin trades above a rising cloud, sized by the cloud's slope, instead of waiting for a breakout day.
Why:
- F1: The book failed on two measures, both from how seldom it holds a position, not from losing trades: its mean daily return is 0.000333 against the 0.0005 required and it trades 0.00695 times per day against the 0.01 required, while its Sharpe (1.117, 0.551 above holding's), its Sharpe with one window left out (0.741) and its Calmar (0.945) all pass.
- F3: The signal is rare because it exists on one bar only: the forecast is non-zero only on the bar of cross age 1, and only when the standardised 60-day return is positive. That gives 64 cases over about 17,400 coin-days (6 coins, 23 to 24 windows, 2,800 to 2,921 bars each), about one bet per coin every 270 days, and leaves the book flat most of the time.
- F5: Earlier runs agree that daily continuation moves outlast their horizon and that a book holding each signal for its horizon pays more often when the move per case covers the cost (findings F9 and F11: 6 of 11 held books against 13 of 58 re-sized ones). This points to staying in the move after the cross rather than acting on the cross day alone.
