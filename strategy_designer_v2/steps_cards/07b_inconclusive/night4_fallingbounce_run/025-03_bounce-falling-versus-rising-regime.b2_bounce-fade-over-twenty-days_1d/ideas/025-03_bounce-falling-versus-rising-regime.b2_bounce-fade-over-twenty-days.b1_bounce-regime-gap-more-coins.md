---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days
line: 7.b inconclusive
backtest: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the 20-day return after a one-day rise of several usual daily moves (its day's return over the standard deviation of its last 20 daily returns) is lower when its 90-day return is negative than when it is positive, and the gap widens as the rise gets larger.
Consequence: A trader would treat a sharp bounce in a coin down over 90 days as a weaker basis for a long over the following weeks than the same bounce in a coin up over 90 days, more so the sharper the bounce.
Why:
- F1: The test's result points the way the idea predicts but falls short of the bar: up-regime minus down-regime 20-day unusual return is +2.17 % with Welch t 1.08 (382 vs 362 cases), and my recomputation gives +1.93 %, t 0.97 (386 vs 362).
- F2: The gap is real in sign but small next to the noise: strength 0.048 of a usual 20-day move (21.24 %), so about 750 cases cannot reach t 2.
- F3: Cost is not the obstacle: the 1.07 % total move per case is 5.5 times the 0.19 % cost of a trade.
- F4: The gap comes almost entirely from the sharpest bounces. In the top quartile of |forecast|, the 20-day gap is +10.1 % (t 1.98; 98 up vs 77 down cases). The lower three quartiles give −0.6 % (t −0.22), +1.0 % (t 0.29) and −2.9 % (t −0.69). The supporting check passed (+3.0 %).
- F6: The idea holds in five of six coins at 20 days, with gaps of +2.0 % to +8.3 % (t 0.47 to 1.17), but none is significant on its own about 125 cases. XRP runs the other way (−8.6 %, t −1.34).
