---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal
line: 7.g patterns
backtest: 016-04_down-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of its hourly path that went into the net rise (net 3-day move over the sum of absolute hourly moves), the more it rises over the next 3 days.
Consequence: Back steady, grinding 3-day rallies and refuse to chase choppy ones of similar size.
Why:
- F4: Over the next 3 days, coins that rose over the past 3 days kept rising more when the rise was efficient (net move over the sum of absolute hourly moves). The slope on efficiency was 0.056 (t 3.30, n 2,865) and is positive in 5 of 6 coins (t 1.0–1.7). By window, it is t 1.29 in w1–w12 and t 3.19 in w13–w24. After controlling for the rise's size and volatility, it is t 1.54. In the top tercile of rises, inefficient rises lost -3.2% excess and efficient ones gained +1.1%.
- F5: The tested measure, the share of a fall carried by its 3 largest hourly losses, explains nothing about the next 3 days (slope t -0.62 on falls, n 2,669). Volume concentration in the 3 biggest hours also adds nothing (t 0.60 on falls, t -1.75 on rises).
