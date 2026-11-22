---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-03_close-below-breakout-bar-low
line: 7.d not profitable
backtest: 029-03_close-below-breakout-bar-low_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes back below its prior 20-day high within 10 days of first closing above it, the coin falls over the next 5 days, and the lower the coin's 20-day volatility of daily returns, the larger the fall.
Consequence: A trader would short failed breakouts in calm coins and stand aside when daily swings are wide.
Why:
- F5: In those same 256 cases, the coin's 20-day volatility grades the outcome the same way. The calm tercile gained +1.01 % (t 1.14), the middle −1.33 % and the volatile tercile −1.55 % (Spearman −0.11). The depth below the old high does not grade it at all: the terciles gave −0.48 %, −0.79 % and −0.59 %, with Spearman −0.007.
- F1: The book trades far too rarely to pay. Its forecast was short on only 63 bars, and it held a position on only 1.76 % of days (257 position-bars across 6 coins × 24 windows). That gives 0.005 trades a day against the required 0.01, and a mean daily return of 0.0052 % against the coins' 0.119 %. That gap is why both the mean-return check and the check against holding fail.
