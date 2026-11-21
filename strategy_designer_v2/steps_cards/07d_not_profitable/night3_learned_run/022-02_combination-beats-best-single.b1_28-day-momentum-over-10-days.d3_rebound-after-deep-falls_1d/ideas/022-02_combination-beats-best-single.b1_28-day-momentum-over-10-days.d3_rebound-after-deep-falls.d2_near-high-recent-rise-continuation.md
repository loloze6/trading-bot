---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls
line: 7.d not profitable
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's close sits in its 60-day close range and the larger its 10-day rise, the higher its return over the next 10 days.
Consequence: A trader would favour longs in coins trading near their 60-day high after a 10-day rise, and avoid longs near the 60-day low.
Why:
- F2: The move after the situation is graded the opposite way from the tested idea. By 28-day return quintile, the unusual 10-day move rises from -1.57 % (deepest falls, t -1.82, 252 cases) to +1.26 % (largest rises). The pooled slope is +1.23 % per standard deviation of the 28-day return (t 2.87, 1259 cases), +1.36 % for the 10-day return (t 3.39, 1547) and +1.24 % for the position in the 60-day range (t 2.27, 827).
- F3: The book's deepest fall is 47.9 % over 261 days (windows w12 to w14). The coins fell 79.6 % over the same stretch, so the book stayed long through a long decline. It held a mean position of 0.45 on forecast-on cells against 0.07 off, which gives a Calmar of 0.07.
- F5: The tested idea is too small to pay: its unusual move is -0.92 % per case over 10 days and its total move is +0.26 %, 1.3 times the 0.19 % cost of a trade. The opposite side is large: among 28-day rises, the middle and top terciles had unusual moves of +1.31 % and +1.66 % (strength 0.087 and 0.104, total +2.5 % and +2.9 %), about 7 to 9 times the cost.
