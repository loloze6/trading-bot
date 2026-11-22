---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, and the smaller the coin's 90-day fall (the closer its 90-day return to zero), the larger the fall.
Consequence: A trader would short sharp bounces in coins that are only mildly down over 90 days, and refuse to short bounces in coins that have already fallen deeply.
Why:
- F1: Before any cost, the book's short bets lose money. Over 5 days the cases' total move in the short direction is −0.21 % (t −1.05, 2989 cases), against a trade cost of 0.22 %. Over 3 days it is −0.33 % (t −2.22) and over 10 days −0.57 % (t −1.99). The 4260 short trades, held 11.1 days on average, lose 3.69 % gross and 3.79 % net each. The failure therefore comes from the move the book captures, not from fees.
- F2: The book is short on 49 % of bars. On those bars it loses 0.042 % a day. Shorting coins whose drift is upward costs 0.100 % a day, and timing gains back only 0.058 %. The idea's unusual move (+0.54 % per case, strength 0.040) is too small to cover a normal drift of −0.75 % in the short direction.
- F3: The fade reverses with the depth of the 90-day fall, against the brief's reading.
- F6: The losses cluster in recovery years.
