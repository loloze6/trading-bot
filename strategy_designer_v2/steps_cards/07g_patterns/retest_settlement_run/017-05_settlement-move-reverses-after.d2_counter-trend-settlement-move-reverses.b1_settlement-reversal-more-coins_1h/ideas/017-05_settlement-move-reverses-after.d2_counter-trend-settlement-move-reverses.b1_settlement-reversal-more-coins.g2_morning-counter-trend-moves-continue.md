---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: During the hours from 03:00 to 11:00 UTC, a coin's 2-hour move that runs against its 24-hour trend keeps going the same way over the next 8 hours, and the larger that 2-hour move, the larger the continuation.
Consequence: A trader follows a counter-trend move made in the Asian and early European hours, instead of fading it, and sizes the trade by the move's size.
Why:
- F4: The tested reversal depends on the time of day, not on funding. A 2-hour move against the 24-hour trend is followed over 8 hours by:
- F5: The 08:00 continuation is negative in all 8 years, at t -1.5 to -4.5 in 7 of them; 2024 is +0.002. Measured as the size of the 2-hour move continuing, it is largest in the top third of 2-hour move size: +0.071 (t 4.35), against +0.042 and +0.019 in the lower two thirds. Over all 08:00 bars, without the trend condition, the 2-hour move does not continue (+0.009, +0.000, -0.006).
- F6: The book enters almost entirely at 07, 15 and 23 UTC. The 07 entries, which sit inside the morning continuation of F4, lose the most: -0.31 % net per trade over 24256 trades. The 15 entries lose -0.12 % over 20092 trades and the 23 entries -0.28 % over 23684.
