---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The wider that stretch was compared with the coin's 30-day average four-hour range, and the larger the coin's 30-day rise, the larger the rise.
Consequence: Weight the rebound buy toward wide broken ranges in coins with a strong monthly rise, and refuse it on narrow breaks in a month that barely rose.
Why:
- F1: The two failed measures come from the weak cases, not from costs. Cases from the narrowest fifth of broken stretches (width 1.0 to 1.9 average 4h ranges) end 18 bars later at -0.86 % against the drift, with a total move of -0.47 % (t -1.46, 125 cases). Cases from the widest fifth (3.7 to 13.5 ranges) end at +2.77 % (t 2.95, 125 cases), a total move of +3.19 %, about 17 times the 0.19 % round trip. The middle three fifths sit between -0.49 % and +0.95 %, so 3 of 5 fifths do not clear the cost on their unusual move.
- F4: The size of the 30-day rise also grades the rebound. Excess return rises steadily across the fifths of the 30-day return, from -1.08 % (just above zero) to +1.74 % (30-day return above +31 %, t 1.98). Narrow stretches in a barely rising month lose -2.04 % (t -2.45, 87 cases), the worst cell of the width-by-30-day table.
- F5: The deep falls behind the 0.47 Calmar sit in the early windows. Windows w3 to w10 have the deepest falls (-16 % to -19 %) and mostly negative book means. Their cases lose: w1 to w3 -1.2 % to -2.7 %, w9 -2.4 %. By year, 2018 cases lose -1.30 % and 2022 cases -1.99 %. From w12 on, no fall is deeper than -10 %.
