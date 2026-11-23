---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses.b1_settlement-reversal-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: During the hours from 14:00 to 24:00 UTC, a coin's 2-hour move that runs against its 24-hour trend is given back over the next 8 hours, and the stronger the 24-hour trend, the larger the move back.
Consequence: A trader fades counter-trend moves only in the US session, in the trend's direction, and sizes the trade by the trend's strength.
Why:
- F4: The tested reversal depends on the time of day, not on funding. A 2-hour move against the 24-hour trend is followed over 8 hours by:
- F6: The book enters almost entirely at 07, 15 and 23 UTC. The 07 entries, which sit inside the morning continuation of F4, lose the most: -0.31 % net per trade over 24256 trades. The 15 entries lose -0.12 % over 20092 trades and the 23 entries -0.28 % over 23684.
