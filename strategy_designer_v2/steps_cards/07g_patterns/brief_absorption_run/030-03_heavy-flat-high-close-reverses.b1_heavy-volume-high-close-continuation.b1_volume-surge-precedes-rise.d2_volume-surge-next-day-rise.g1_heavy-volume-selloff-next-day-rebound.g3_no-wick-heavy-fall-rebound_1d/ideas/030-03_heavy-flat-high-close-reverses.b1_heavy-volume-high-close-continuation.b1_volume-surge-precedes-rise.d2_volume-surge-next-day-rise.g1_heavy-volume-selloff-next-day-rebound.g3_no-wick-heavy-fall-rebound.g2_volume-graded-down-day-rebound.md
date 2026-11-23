---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a down day's volume is against its prior 20-day average, the more the coin rises over the next day.
Consequence: A trader buys for one day after down days in proportion to how far their volume exceeds its recent average, and refuses the down days of ordinary volume.
Why:
- F2: Across all down days, the next-day excess return rises with the day's volume against its prior 20-day mean, but only at the top: the top volume quintile gave +0.76 % (t 4.84, 1435 cases), while the four lower quintiles gave −0.04 % to +0.13 % (t −0.36 to 1.05).
- F6: The rebound lasts one day: trades held about 1 day earned +1.50 % net (2201 trades), while trades kept open 2, 3 and 4 days, which the forecast extended through further heavy down days, lost −2.95 % (513), −6.89 % (119) and −11.74 % (31).
- F7: The tested close-position effect needs heavy volume: on light-volume down days the quintiles of fall left at the close gave −0.14 % to +0.16 % (all |t| ≤ 1.01), against −0.13 % to +0.87 % (t up to 4.45) on heavy-volume down days.
