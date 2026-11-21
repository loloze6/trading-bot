---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
line: 7.b inconclusive
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The wider that stretch was compared with the coin's 30-day average four-hour range, the larger the rise.
Consequence: In a coin that has risen over the past month, buy a break below a wide two-day range rather than short it, and refuse the short most firmly when the broken range was wide.
Why:
- F1: The main measure is on the side the idea predicts but small: the mean 18-bar excess return is +0.24 % with t 0.97 over 1182 independent cases, a strength of 0.023. At 6, 12 and 36 bars it is +0.07 %, +0.10 % and +0.04 %, all with t below 1, so no other horizon clears it either.
- F5: The effect is mixed across periods, which drowns the pooled mean:
- F6: By coin the pooled result is mixed. BTC (-0.36 %) and XMR (-0.29 %) are negative, while LTC (+0.98 %, t 1.77), ETH (+0.59 %) and ZEC (+0.54 %) are positive. Among the widest-forecast cases, 5 of 6 coins are positive (ZEC +3.79 %, t 2.37); BTC is the exception at -0.70 %.
