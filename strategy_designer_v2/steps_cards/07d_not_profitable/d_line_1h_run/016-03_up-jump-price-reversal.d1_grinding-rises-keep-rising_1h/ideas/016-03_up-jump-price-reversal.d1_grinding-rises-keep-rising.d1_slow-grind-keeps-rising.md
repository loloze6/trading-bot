---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the smaller the share of that rise that came from its few biggest hourly gains (a grind of many small hourly steps), the more the coin keeps rising over the next 3 days. This holds with evenness judged on the whole 3-day rise against the coin's usual evenness over the past several weeks, so it changes only as slowly as the 3-day rise itself, and the effect is larger the larger the rise.
Consequence: A trader would hold a long through a grinding 3-day rise for days, sized by its evenness and its size, instead of re-trading it every few hours and paying fees that exceed the gain.
Why:
- F1: Fees, not the forecast, sink the book. The gross gain is 0.000013 per bar against 0.000034 per bar of fees, so fees run about 2.6 times the gross gain. That turns a holding Sharpe of 0.55 into a book Sharpe of -1.02, with a mean daily return of -0.000522 and only 27% of days positive.
- F2: The signal flips on an hourly scale while its idea is a 3-day one. Over 20,233 trades the median trade lasts 5 hours. Each window has about 50 long spells averaging 9.7 hours, the forecast moves 0.67 points per bar on average, and turnover is 0.031 of the book per bar. This churn comes from standardising the evenness against only its own last 72 values.
- F3: The forecast is mostly all-or-nothing. 46,969 active bars sit in the 15–20 bin against 5,231–8,308 in each lower bin. Half of the rising 3-day grid cases get a forecast of 0, and those cases have excess forward returns of -0.0024 and -0.0007.
- F4: Where the forecast is strongest, the slow effect does exist. On the non-overlapping 72-hour grid of rising coins, the quarter with the smallest top-3-gain share has a next-3-day excess return of +0.0107 (t 3.21, n 717), falling steadily to -0.0044 in the quarter with the largest share. The top forecast quarter (mean forecast 19) earns +0.0073 (t 2.19).
- F5: Much of that evenness effect is the size of the rise. Among rising cases the evenness term has t 3.12 alone but t 1.76 next to the 3-day return (t_past 1.05). Within the largest-rise tercile both evenness halves earn about +0.008, while in the smallest-rise tercile both lose (-0.0068 and -0.0029).
