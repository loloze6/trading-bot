---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 10 days is larger the thinner the cloud (the gap between its two spans as a share of the price).
Consequence: A trader would keep a thin-cloud breakout on for about ten days rather than five, capturing the second half of a move that is still rising at twice the tested horizon.
Why:
- F1: The book fails on its mean daily return (0.000459 against the 0.0005 required), while holding the coins earns 0.00118 a day; the book holds a position on only 28 % of bars, at a mean allocation of 0.54 when in (0.15 over all bars), so it is out of the coin most of the time. Its gain per bar splits into 0.000179 from the market's own rise and 0.000301 from timing.
- F2: Cost is not what loses the gain: per case the total 5-day move is +1.85 % against a round trip of 0.19 % (9.6 times), and the unusual move is +1.28 % (6.6 times).
- F4: Inside the above-rising-cloud regime the move outlasts the 5-day horizon. The mean return grows from +1.39 % over 5 days to +2.91 % over 10. By forecast quartile, the 10-day return is +0.5 %, +2.5 %, +2.4 % and +6.2 %, against 5-day excess returns of -0.57 %, +0.27 %, +0.19 % and +3.31 % (about 170 cases each).
