---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The wider that stretch was compared with the coin's 30-day average four-hour range, and the higher the coin's 7-day volatility against its 30-day volatility, the larger the rise.
Consequence: Buy the break below a two-day range in a rising month mainly when the range was wide and volatility has just picked up, and leave narrow, calm breaks alone.
Why:
- F1: The two failed measures come from the weak cases, not from costs. Cases from the narrowest fifth of broken stretches (width 1.0 to 1.9 average 4h ranges) end 18 bars later at -0.86 % against the drift, with a total move of -0.47 % (t -1.46, 125 cases). Cases from the widest fifth (3.7 to 13.5 ranges) end at +2.77 % (t 2.95, 125 cases), a total move of +3.19 %, about 17 times the 0.19 % round trip. The middle three fifths sit between -0.49 % and +0.95 %, so 3 of 5 fifths do not clear the cost on their unusual move.
- F2: A rise of the coin's recent volatility grades the rebound as strongly as width does. Cases where the 7-day volatility is highest against the 30-day volatility (ratio 1.21 to 1.91) end at +2.73 % against the drift (t 3.02, 124 cases); the four lower fifths end between -0.50 % and +0.17 %. At bar level, the position earns 0.067 % per held bar in that top fifth and about 0.000 % in the two lowest fifths, where the book still holds 17 to 26 % allocation.
- F3: Width and the volatility rise together carry the effect. Wide stretches with a high volatility ratio end at +2.91 % (t 3.26, 130 cases). Wide stretches with a low volatility ratio end at -3.07 % (t -2.45, 20 cases), and every narrow-stretch cell is negative (-0.60 % to -0.77 %). Across cases, the Spearman correlation with the excess return is 0.143 for raw width and 0.134 for the volatility ratio, against 0.078 for the book's forecast, which re-standardises width against its own past 180 values.
- F6: The book's trades are not eaten by fees. There are 2683 trades, with a mean of +1.18 % gross and +1.08 % net and a 67 % hit rate, and they last a median 72 hours. The low mean daily return (0.025 % against 0.05 %) comes from small allocations and from taking the many weak cases, not from cost.
