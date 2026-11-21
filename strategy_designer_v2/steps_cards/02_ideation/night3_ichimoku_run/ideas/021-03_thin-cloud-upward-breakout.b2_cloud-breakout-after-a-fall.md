---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-03_thin-cloud-upward-breakout
line: 7.b inconclusive
backtest: 021-03_thin-cloud-upward-breakout_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that crosses up from below a coin's Ichimoku cloud to above it, the coin rises over the next 26 days, and the more the coin fell over the past 26 days before the cross, the larger the rise.
Consequence: An upward cloud cross that follows a fall is a reason to go long for the next few weeks, while a cross that comes after a run-up is a reason to refuse that trade.
Why:
- F3: The thinness grading, the brief's own claim, is absent. The thin-minus-thick difference is +0.23 %. The rank correlation of cloud proximity with the unusual 26-day return is −0.02 (raw) and +0.02 (standardised). The raw-proximity quartiles run +0.9 %, +6.5 %, +12.4 %, −0.3 % with no order. More data would not make this grading appear.
- F5: The horizon is not the problem. The unusual return is +0.9 % at 5 days (t 1.01), +2.4 % at 10 days (t 1.62) and +4.9 % at 26 days (t 1.55). At 52 days it vanishes (−0.5 %, t −0.08, 112 cases), so the move is built within the plan's 26 days and fades afterwards.
- F6: The rise after a cross is larger the more the coin had fallen over the 26 days before it. By quartile of the past 26-day return, the mean unusual 26-day return runs +12.6 % (t 1.38, 59 % positive), +10.1 %, +5.6 % and −4.2 % (t −1.00, 33 % positive), with 27 cases each. The 52-day past return shows no such order.
- F7: Cost does not explain the failing book. The total move per case (+9.44 %) is 48.9 times a round trip's 0.19 %. The book's Sharpe is 0.92, 0.35 above holding the coin. It fails on mean daily return (0.00044 against 0.0005) and Calmar (0.68 against 0.75), which fits the skewed, year-driven returns of F1 and F2.
