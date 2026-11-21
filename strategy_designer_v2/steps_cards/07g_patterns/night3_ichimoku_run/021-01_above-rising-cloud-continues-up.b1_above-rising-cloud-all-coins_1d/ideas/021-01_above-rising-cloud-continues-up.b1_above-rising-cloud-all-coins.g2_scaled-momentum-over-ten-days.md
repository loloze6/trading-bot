---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's return over the past 26 days, scaled by its daily volatility over the same 26 days, the larger its return over the next 10 days.
Consequence: A trader sizes a 10-day position with the coin's volatility-scaled 26-day return, long after the strongest rises and away from coins after the steepest falls.
Why:
- F2: The same 26-day return ranks the next 10 days even more clearly: Spearman 0.084 (p < 0.0001, 2619 cases), with the top fifth +3.4 % and the bottom fifth −1.9 % against drift (t 4.02); taking the 26-day return over its own volatility gives about the same (Spearman 0.080); and it survives a control for the cloud regime (regression t 3.82, regime t 2.71).
- F4: Momentum's signal is far larger than a trade's cost: taken in the direction of the 26-day return, the unusual move is +5.6 % per case after rises (strength 0.14, t 2.61, 439 cases) and +3.4 % after falls (strength 0.08, t 1.95, 449 cases), 15 to 25 times the 0.22 % round trip and above the 0.05 strength of F10, while the tested cloud-slope idea's was +1.00 % (strength 0.018) and its book trailed holding (Sharpe 0.56, 0.03 below holding; 3.7 bps a day against the coins' 14).
