---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
line: 7.d not profitable
backtest: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close above the prior 20-day high is followed within 3 days by a close back below that high, the coin falls over the next 5 days, only while the coin is calm: the lower its 30-day daily volatility at the failure, the larger the fall.
Consequence: A trader would short failed breakouts in quiet markets and refuse them when the coin is volatile, where the failure is usually followed by a rebound.
Why:
- F1: The idea's effect is not in the data. On my own non-overlapping recount of failed breakouts, the unusual short-direction move over 5 days is -0.26 % per case (t -0.36, 245 cases), and step 5 measured -0.36 % (t -0.85, 641 cases). Failed breakouts are therefore followed by slightly more rise than the coin's normal drift, not by a fall.
- F2: The book loses because it is short against a rising market. Its mean gain is -0.000323 per bar, and -0.000247 of that comes from being short while the coins drift up; timing adds only -0.000077. It holds a position on 21 % of bars, at a mean allocation of -0.93.
- F4: The fall appears only in calm coins and grows as volatility falls. By quintile of the coin's 30-day daily volatility, the unusual 5-day short move runs +2.05 % (t 1.87, 49 cases) in the calmest fifth, then +0.84 %, -0.07 %, -0.74 %, and -3.40 % (t -1.39) in the most volatile fifth. The slope on volatility is -0.62 (t -1.79, Spearman -0.12, p 0.057).
- F5: The book loses most in the volatile states, despite vol-target sizing.
- F6: The calm-coin fall is not carried by one period. Among cases below the median volatility, the unusual move is positive in 65 % of the 23 windows that have such cases, and positive or flat on five of six coins (XMR +3.40 %, ZEC +2.96 %, BTC +0.98 %; ETH -0.25 %).
