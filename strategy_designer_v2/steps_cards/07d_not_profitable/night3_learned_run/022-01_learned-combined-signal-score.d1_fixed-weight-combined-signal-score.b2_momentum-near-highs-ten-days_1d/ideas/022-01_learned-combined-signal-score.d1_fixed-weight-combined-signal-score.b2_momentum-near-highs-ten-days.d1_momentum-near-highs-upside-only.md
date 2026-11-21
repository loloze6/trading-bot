---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b2_momentum-near-highs-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 28-day return plus its closeness to its 90-day high, the higher its return over the next 10 days, the rise above the coin's usual drift growing with how far both stand above their usual level.
Consequence: A trader would lean long a coin only as far as its four-week rise and nearness to its three-month high exceed their usual level, more so the stronger they are, rather than shorting coins where they are weak.
Why:
- F1: Only the long side pays. On 8,544 long bars the book earns +8.2 bps a day (t 4.7), of which +4.7 is timing. On 8,640 short bars it earns −0.7 bps (t −0.58): their +1.9 bps of timing is more than eaten by −2.7 bps of the coins' own rise. Counting the long bars alone gives 4.0 bps a day per coin-bar, against 3.65 for the whole book.
- F2: Almost all the gain comes from the strongest forecasts. The top forecast quintile (mean forecast 8.2) earns +17.6 bps a day (t 4.5), while the other four earn between −1.7 and +2.2 bps. On the 10-day grid, the top three deciles end +1.5 % to +2.1 % above drift (169 cases each). The middle is not graded: decile 6 ends −1.27 % and decile 0 ends −0.39 %.
- F6: Longs are graded by nearness to the high and by the 4-week rise.
- F8: The book lags holding in bull windows. It earns in 15 of 24 windows, but in w11 it made +7.4 % against holding's +281 %, and in w21 +19 % against +87 %.
