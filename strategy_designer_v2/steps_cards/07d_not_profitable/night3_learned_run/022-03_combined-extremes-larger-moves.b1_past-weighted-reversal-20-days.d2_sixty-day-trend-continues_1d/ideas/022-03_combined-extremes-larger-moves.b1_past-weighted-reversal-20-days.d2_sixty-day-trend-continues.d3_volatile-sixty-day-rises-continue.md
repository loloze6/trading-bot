---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
line: 7.d not profitable
backtest: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 60-day rise, the more the coin rises over the next 20 days, the more so the higher its 20-day volatility.
Consequence: A trader would hold longs after large 60-day rises, sizing up when the coin is volatile, and would not take the short side.
Why:
- F1: The book's shorts cost it most of holding's gain. Over 17,432 coin-days short, the shorts earned −0.069 % a day before fees. Of that, −0.078 % came from being short coins that drift up, and only +0.009 % from timing. Over 16,188 days long, the longs earned +0.122 % a day, with +0.032 % from timing. As a result the book makes 0.029 % a day against holding's 0.139 %, and fails the mean-return and Sharpe-against-holding measures.
- F6: Longs pay mainly when the coin is volatile. By 20-day-volatility tercile, the unusual move for longs is −0.4 %, +1.9 % and +6.6 % per case (total 2.6 %, 5.0 %, 10.1 %; about 220 cases each). Daily long gains before fees rise from 0.072 % to 0.268 % from the lowest to the highest tercile.
- F2: The deepest fall is −78 %, lasting 735 days from w15 to w21. Across those windows the summed daily returns were −1.32 for the book and +0.85 for holding. The book sat about half long and half short (long share 0.49, net position +0.04). On the 20-day grid in w15–21, shorts lost 5.6 % per case against the coin's drift (t −3.06, 202 cases) and longs lost 1.0 % (289 cases). In the other windows, shorts gained 3.5 % (t 3.94, 601 cases) and longs 2.5 % (514 cases).
