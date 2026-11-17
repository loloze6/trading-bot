---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side
line: 7.e profitable but not proven
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the higher its daily volume relative to its own 20-day average volume, the higher its return over the next 3 days.
Consequence: A rising coin trading on unusually heavy volume is a reason to be long for the next few days, and a rising coin on thin volume is a reason to refuse the trade.
Why:
- F7: Inside the rising-month regime, the gain follows heavy volume. On bars whose volume is in the top third relative to its 20-bar mean, the 3-bar excess return is 0.01265 (t 3.72, n 876) and the 7-bar is 0.0190 (t 2.17, n 362). The lowest third gives 0.0014 at 3 bars and -0.0043 at 7 bars.
- F4: The edge is strongest at a shorter horizon than the plan's 7 bars. The Welch t of active bars minus flat bars is 2.91 at 3 bars (2798 active cases, active mean excess 0.00318, t 1.92), 2.58 at 7 bars and 1.83 at 1 bar. It fades to 0.98 at 14 bars and 0.70 at 30 bars.
- F1: The book earns a mean daily return of 0.000635. Of that, 0.000287 comes from the market's own rise and 0.000348 from timing, while holding the coins earned 0.001230 a day. The book therefore keeps only about half its gain from timing and trails holding in raw return.
