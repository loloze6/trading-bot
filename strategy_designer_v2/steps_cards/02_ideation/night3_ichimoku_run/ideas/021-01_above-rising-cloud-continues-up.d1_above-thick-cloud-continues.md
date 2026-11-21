---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 26 days is positive, and larger the thicker the cloud (the gap between its two spans as a share of the price) rather than the faster the cloud has risen. The cloud is the band between the average of the 9-day and 26-day high-low midpoints and the 52-day high-low midpoint, plotted 26 days ahead.
Consequence: Inside the above-rising-cloud situation, a trader would put more weight on a coin standing above a thick cloud than above a thin one.
Why:
- F3: The idea's situation does separate. On the non-overlapping 26-day grid, the 149 cases above a rising cloud return +8.6 % (excess +4.8 %, t of the raw return 2.30). The 427 other grid cases return +2.5 % (excess −1.7 %).
- F4: The idea's grading does not work: a faster-rising cloud does not mean a larger move. The forecast (the cloud's 26-day rise, standardised) has a Spearman rho of −0.07 with the excess return. Its quartiles of about 37 cases give +3.6 %, +6.3 %, +7.0 % and +2.5 %, and the verdict's slope t is 0.05. Position size therefore follows a variable that carries no information.
- F5: Inside the active cases, a thicker cloud comes before larger moves. Cloud thickness relative to price has a rho of +0.11. Its quartiles give an excess of +19.2 %, +4.8 %, +23.0 % and +36.7 %, so the thickest quarter does best. The brief expected thin clouds to move more.
- F1: The book earns 3.6 bps a day against 11.8 bps for holding the coins (Sharpe 0.45 against 0.55). Its mean position is only 0.25 of the book, although it is long on 76 % of days. Of its 3.6 bps, 2.95 bps come from the market's own rise and only 0.68 bps from timing. The failing gain is mostly the coin's drift taken at a quarter size, with almost no timing edge.
