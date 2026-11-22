---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling
line: 7.d not profitable
backtest: 024-04_downrun-volume-fade-depth-rebound.b2_dips-in-downtrends-keep-falling_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of falling four-hour periods whose loss is large relative to the coin's typical four-hour move over the past 30 days, the coin keeps falling over the next three days. This holds only while the coin's 30-day return is negative and its 30-day fall is small against its usual 30-day move. Within that, the closer the 30-day fall comes to the coin's usual 30-day move, the larger the further fall.
Consequence: A trader leans short on sharp drops only in moderate monthly downtrends and refuses the short once the monthly fall is deep, where the coin rebounds instead.
Why:
- F3: The idea's grading by the 30-day return runs the wrong way at the deep end. Cases with a 30-day return below -25 % have strength -0.107 (t -2.01, 496 cases, -0.82 % unusual move). That is a rebound against the short. Cases between -25 % and -2.4 % have strength +0.07 to +0.10 (t 1.76 to 2.44).
- F4: On the non-overlapping 18-bar grid of all bars, a 30-day return below -25 % is followed by a mean 3-day rise of +1.07 % (t 2.53, 511 cases). A 30-day return between -25 % and -15 % is followed by -0.76 % (t -2.17, 466 cases).
- F5: The forecast's size carries no information. The strongest forecast bucket (-20 to -14.3, 2048 cases) has strength 0.014 (t 0.65). The largest streak losses (2.4 to 26 usual moves) have strength 0.007 (t 0.18). The cube transform therefore puts most of the book's size where there is no edge.
- F6: The book keeps its shorts well past the 3-day horizon, with a mean trade length of 327 hours.
