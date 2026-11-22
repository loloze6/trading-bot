---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b1_downtrend-bounce-more-coins.b1_outsized-downtrend-bounces-given-back_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, only while its 30-day return is negative. The fall grows steeply both with the size of the rise in usual daily moves and with the depth of the 30-day fall.
Consequence: A trader would fade outsized bounces only in coins deep in a fresh 30-day fall, sized by bounce size times fall depth, and would stop shorting falling-on-90-days coins that have already recovered over the last month.
Why:
- F2: The fade exists only in coins that are also deep in a 30-day fall. Among rises of more than 1 usual daily move in falling coins, those whose 30-day return is in the lowest third (below -12.7 %) are followed by a large unusual fall:
- F3: Inside that deepest 30-day third the fade grows with the bounce. Rises of 1–1.75 usual moves give 3.7 % (t 2.34, n 84), 1.75–2.5 give 4.3 % (t 1.93, n 21), and above 2.5 give 11.5 % (t 4.44, n 11). The product of the bounce size and the 30-day fall depth grades the same way: its top quartile gives 4.8 % (t 3.09, n 87) and its two lowest quartiles about -0.4 %.
- F4: Where the 90-day return is negative but the 30-day return is positive, the shorts lose. Bounces of 1–1.75 usual moves in the top 30-day third (above +4.4 %) give -3.0 % unusual (t -2.06, n 75). The book's short bars in the top 30-day quartile (above +6.9 %) average -0.149 % per bar, summing to -4.71, against +0.09 % per bar in the two lowest quartiles.
- F5: The 90-day return, which defines the regime, does not grade the effect. Rises of more than 1 usual move give -0.1 % (t -0.05), 1.0 % (t 0.56) and 1.4 % (t 0.70) across its three terciles (30 cases each).
- F1: The book loses because being short costs more than its timing earns. Per bar it makes -0.017 %. Before fees that is -0.011 %, which splits into -0.029 % from shorting coins whose average daily return is positive and +0.018 % from timing, plus 0.006 % of fees. The book is short on 44 % of bars, at a mean of -0.45 of the book.
