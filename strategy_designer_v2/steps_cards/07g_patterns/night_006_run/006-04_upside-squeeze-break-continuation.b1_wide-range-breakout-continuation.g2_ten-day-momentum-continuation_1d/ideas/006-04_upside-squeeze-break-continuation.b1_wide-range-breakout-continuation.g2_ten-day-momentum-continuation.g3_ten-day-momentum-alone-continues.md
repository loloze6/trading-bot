---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g2_ten-day-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 10-day return, the further its price rises over the next 10 days.
Consequence: A trader would size longs by 10-day momentum alone and drop range position, and would hold shorts back since the short side lost in a rising market.
Why:
- F3: Range position adds nothing once the 10-day return is known. In a joint regression of 10-day excess return, the 10-day return has t=3.31 and the position in the 20-day range has t=-0.19 (about 1,690 cases).
- F4: The idea's edge is unstable over time. The forecast's slope t by year runs from -2.54 (2018) to +3.53 (2020), with negative t in 2021-2023 territory (0.52, -0.68, -0.81). The top range-position quintile beats the rest by -0.032 in 2023 (t=-2.23).
- F6: The book earns 0.000163 a day. Only 0.000033 of that comes from the market's rise; nearly all its gain sits in the most-long position quintile (book +0.00125 a day at mean allocation +0.47). The most-short quintile loses -0.00061 a day while coins rise +0.0010.
