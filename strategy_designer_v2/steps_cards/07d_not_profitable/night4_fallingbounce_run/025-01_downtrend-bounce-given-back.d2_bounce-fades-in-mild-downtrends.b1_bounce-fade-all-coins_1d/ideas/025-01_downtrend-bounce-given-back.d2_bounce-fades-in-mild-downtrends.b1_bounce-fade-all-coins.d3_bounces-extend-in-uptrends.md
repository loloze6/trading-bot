---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends.b1_bounce-fade-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, a one-day rise that is large relative to its 20-day standard deviation of daily returns is followed by a further rise over the next 5 days. The larger the rise against its usual daily move, the larger the rise that follows.
Consequence: A trader would buy sharp up-days in rising coins rather than fade them.
Why:
- F5: In coins outside the falling regime, a one-day rise of more than 2 usual daily moves is followed by a further rise of +5.25 % over 5 days (t 4.84, n 495), or +4.46 % beyond drift (t 4.13). That is about 24 times the cost of a trade, and it is the opposite of what follows bounces in falling coins.
- F6: The size of the rise does not grade the fade cleanly. Total 5-day short moves by quartile of the day's scaled rise are +0.45 %, +0.46 %, −0.77 % and +0.72 %, so only the largest rises carry a fade (+1.50 % unusual, t 2.72).
