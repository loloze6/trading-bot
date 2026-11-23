---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rises after falling over the past 24 hours, by more the larger that fall is against its usual 24-hour move. The rise is larger the more that day's volume exceeds its daily average over the past 7 days.
Consequence: A day-long fall on heavy volume is a reason to be long for the next day, sized by the fall and by the volume surge.
Why:
- F3: A fall is reversed more when it came on heavy volume. When the 24-hour volume is in the top third against its 7-day daily pace, the fall's size correlates −0.180 with the next-day excess return (t −13.6, 5 560 cases, mean +0.075 usual moves). In the lowest third, the correlation is −0.063 (t −4.8, mean −0.026).
- F1: On a non-overlapping daily grid over all coins and windows, a coin's 24-hour return, counted in its usual 24-hour moves, correlates −0.067 with its excess return over the next 24 hours (t −12.7, 35 122 cases). The reversal sits in the coin's most volatile third of its 7-day hourly volatility: corr −0.125 (t −13.6), and among falls alone corr −0.161 (t −12.4), with a mean next-day excess of +0.115 usual moves. In the calmest third, falls have −0.042 usual moves and corr +0.027.
- F7: Size against cost. A fall in the volatile third earns +0.115 of a usual 24-hour move (about 5.5 %), which is about 0.6 % per case, near 2.9 times the 0.22 % cost of a trade. The tested idea's strength was 0.024 (an unusual move of 0.6 times the cost).
