---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's 7-day volatility is above its usual level, the larger its 1-day fall measured against that volatility, the more the coin rises over the next 3 days.
Consequence: A trader should buy sharp one-day falls in volatile markets, sized by the fall, and refuse to sell them.
Why:
- F4: The larger a coin's 1-day fall, measured in its recent volatility, the larger its rise over the next 3 days. The bottom decile of 1-day returns gives a strength of 0.133 (t 4.64, 1135 cases), and among falling days the slope of strength on the 1-day z-return is −0.106 (t −4.55, 4596 cases). The rebound is concentrated in high volatility: 0.282 (t 6.22, 464 cases) when 7-day volatility is above its usual level for the coin, against 0.047 (t 1.11, 485 cases) below it. It is positive in 5 of 8 years.
- F1: When a 4h bar closes below the low of the prior 2 days (12 bars), the coin rises more than usual over the next 3 days. The strength is 0.168 (t 4.44, 753 independent cases), an unusual move of +1.60 % and a total move of +2.13 %, which is 7.3 and 9.7 times the 0.22 % round-trip cost. Over 12 days the strength is 0.284 (t 4.70, 173 cases), with an unusual move of +5.01 % and a total of +7.27 %. Over 1 day there is no effect (−0.008, t −0.32, 2132 cases).
