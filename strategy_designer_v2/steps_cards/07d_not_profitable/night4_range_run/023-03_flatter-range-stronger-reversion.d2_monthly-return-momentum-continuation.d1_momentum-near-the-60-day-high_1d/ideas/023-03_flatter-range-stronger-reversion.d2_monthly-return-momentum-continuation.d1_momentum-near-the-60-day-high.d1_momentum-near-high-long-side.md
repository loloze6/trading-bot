---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 30-day return, the larger its rise over the next 5 days, the more so the closer the coin's close stands to its highest close of the past 60 days, only while the 30-day return is positive.
Consequence: A trader leans long on monthly strength near the 2-month high and does not short monthly weakness, which removed nothing but losses in the deepest falls.
Why:
- F1: The Calmar of 0.51 fails because one fall is far deeper than the rest: the chain of daily returns falls 51.6 % over 888 days (w1 to w11, book −50.7 % while the coins fell −59.6 %), against a yearly return of 26.3 %; the next deepest falls are −33.0 % (w12–w16), −19.1 % (w19–w21) and −18.5 % (w21–w23).
- F2: The short side earns nothing and deepens the falls. Over 4698 short bars the position's gain is a mean of −0.013 % (t −0.45, sum −0.61), against +0.18 % (t 5.08, sum +15.2) over 8325 long bars. In the deepest fall, shorts lost −2.67 against −0.67 for longs, and every coin's short side lost (LTC −0.74, XRP −0.64, ZEC −0.57).
- F3: The shorts lose most after the largest monthly falls. The short bars in the lowest 30-day-return quintile (mean −36 %) average −0.12 % per bar (sum −0.94), against +0.02 % to +0.06 % in the middle quintiles. A coin far below its high after a big monthly drop did not keep falling.
- F7: The losses are not a problem of size against cost. Per case the total move is +1.13 % and the unusual move +0.95 % (strength 0.087), 5.8 and 4.9 times the 0.19 % cost of a trade. The failure is the depth of the falls, carried by the shorts and by over-extended longs.
