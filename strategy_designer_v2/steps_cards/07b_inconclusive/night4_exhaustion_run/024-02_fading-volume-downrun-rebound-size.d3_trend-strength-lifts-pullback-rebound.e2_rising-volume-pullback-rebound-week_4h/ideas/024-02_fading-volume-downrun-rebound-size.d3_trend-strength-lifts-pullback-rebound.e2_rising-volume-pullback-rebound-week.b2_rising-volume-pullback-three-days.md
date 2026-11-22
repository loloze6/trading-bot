---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin with a positive 30-day return falls in a streak of four-hour periods on rising volume, it rises over the next three days, and the more the volume rose across the streak, the larger that rise.
Consequence: A trader buys pullbacks within an uptrend that come on growing volume and holds them for about three days rather than a week, where the rebound shows before the market's noise dilutes it.
Why:
- F2: The effect is clearer at shorter horizons than the plan's seven days: over 18 bars (3 days) the unusual move is +0.54 % with t 2.37 over 1,397 cases (strength 0.067, t 2.50), and over 6 bars (1 day) it is +0.27 % with t 1.95 over 1,415 cases. Over 42 bars it is +0.46 % (t 1.23), and over 84 bars +0.63 % (t 1.07): the move grows little after three days while the market's noise grows.
- F3: The supporting check could not be computed because 77 % of cases have a forecast at the +20 cap, so the median equals the cap and no case is above it. On the recorded size of the volume-rise component, the larger half beats the smaller half by +0.77 % at 42 bars. That grading comes from the weakest quartile alone: it loses −1.23 % (t −1.87, 335 cases), while the other three gain +1.36 %, +0.89 % and +0.80 %.
- F5: No single coin carries the 7-day result. Five of six coins are positive at 42 bars, with none reaching t 1.05: BTC +0.59 % (250 cases), ETH +0.69 %, ZEC +1.21 %, XMR −0.06 %, XRP +0.02 %. At 18 bars all six are positive, ETH reaching t 2.17.
