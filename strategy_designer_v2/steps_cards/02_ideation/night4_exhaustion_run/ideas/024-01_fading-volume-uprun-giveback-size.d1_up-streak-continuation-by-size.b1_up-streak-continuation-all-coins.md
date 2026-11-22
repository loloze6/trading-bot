---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size
line: 7.b inconclusive
backtest: 024-01_fading-volume-uprun-giveback-size.d1_up-streak-continuation-by-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just risen in an unbroken streak of four-hour periods, it keeps rising over the next three days, and the larger the streak's gain relative to the coin's typical four-hour move over the past 30 days, the larger the further rise.
Consequence: A strong 4-hour up-run is a reason to join it for three days rather than to fade it.
Why:
- F1: The main measure is on the side the idea predicts but short of the bar: the forecast-weighted excess 18-bar return is +0.0029, with t 1.21 over 2857 grid cases. The supporting check passed. The size is nil: the unusual move is −0.09 % per case (strength −0.009), against a cost of 0.19 % per trade.
- F2: The effect is mixed by forecast size, not graded smoothly. The bottom three forecast quintiles have excess 18-bar returns of −0.16 %, −0.36 % and −0.40 % (t −0.50, −1.11, −1.20). The top two quintiles together have +0.58 % (t 2.04, n 1111). The top 40 % of forecasts carry +0.58 % (t 2.10, n 1143, strength 0.065), while the rest carry −0.25 % (t −1.34, n 1714).
- F5: The sign is the same across coins but no single coin is clear. Each of the six coins has a positive top-forecast excess, from +0.15 % (BTC) to +1.30 % (XRP), with every t between 0.26 and 1.57 and about 170 to 220 cases per coin.
