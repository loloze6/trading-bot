---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the larger that rise in units of the usual daily move, the larger the fall, only while the coin's 30-day return is also negative, the fall being larger the more moderate that 30-day decline.
Consequence: A trader would fade bounces when the past month's decline is still under way but not yet a capitulation, and skip them when the past month has already turned up.
Why:
- F5: A moderate 30-day fall marks where the bounce is given back. Short cases with a 30-day return between -30 % and -15 % have an unusual move of +3.04 % (t 6.44, 413 cases), and between -15 % and 0 % +1.37 % (t 3.30). Cases with a 30-day fall beyond -30 % give only +0.83 % (t 0.85), and cases with a positive 30-day return give negative moves (-0.78 % and -0.43 %).
- F2: The coin's own rise eats the timing gain. On the 16,212 short bars the part from the market's own rise is -0.066 % a day and timing is +0.041 %, so the short bars net -0.025 %. Per case, the total move is -0.14 % against a cost of 0.22 %, even though the unusual move is +0.62 % (t 2.81, 2,312 cases).
- F3: The effect sits in shallow 90-day falls and reverses in deep ones. Cases with a 90-day return between -10 % and 0 % have an unusual short move of +2.60 % (t 3.97, 97 cases) and a total move of +1.87 % (t 2.90). Cases between -25 % and -10 % give +1.78 % (t 2.59). Cases below -45 % give -0.96 % unusual and -1.73 % total (119 cases). The book's short bars earn +0.24 % a day at -10 % to 0 % and lose -0.04 % a day below -45 %.
