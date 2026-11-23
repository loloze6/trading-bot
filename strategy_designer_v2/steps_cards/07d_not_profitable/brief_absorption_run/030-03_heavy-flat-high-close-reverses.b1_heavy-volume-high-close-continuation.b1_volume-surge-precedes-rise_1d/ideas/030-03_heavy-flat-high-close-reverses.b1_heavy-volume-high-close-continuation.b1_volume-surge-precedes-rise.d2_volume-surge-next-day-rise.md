---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a day relative to its own prior 20-day average, the more the coin rises over the next day.
Consequence: A trader holds long only for the day after a heavy-volume day, more so the larger the surge, instead of sitting long through the quiet days that follow.
Why:
- F3: The gain sits on the days the volume is heavy, not on the 10 days held after them: on bars with a positive forecast (6703) the next day's coin return is +0.29 % and the position's gain +0.25 % per bar (summed 16.8); on the bars held within 10 days after a signal (9423), the next day's coin return is +0.003 % and the gain +0.035 % per bar (summed 3.3), so most of the exposure that carries the falls earns almost nothing.
- F4: Holding is already too long at 10 days. On the 10-day grid the strongest forecast bucket (>1.5) has a mean excess of +1.03 % (t 1.58, n 639); on the 20-day grid it has only +0.41 % (t 0.29, n 284). Cutting the hold to 5 bars raised Calmar only to 0.58 (deepest fall -55.5 %), so the gain lies at a horizon shorter than the holds tested.
- F2: The book stays long almost all the time: it is in a position on 90 % of the coins' days, holds a mean allocation of 0.49 even on grid bars with no signal, and 85 % of grid bars carry a long allocation, so in a bear market it takes most of the coin's fall.
- F1: The failing measure is the falls. The book's deepest fall was -58.4 %, from w12 to w14 over 276 days, while the coins fell -81.2 %; its second was -54.0 %, from w1 to w3 over 309 days, while the coins fell -66.4 %; both were long bear stretches (book mean daily return -0.17 % in 2018 and -0.13 % in 2022), against a yearly return of +31.1 %, giving a Calmar of 0.53 against the 0.75 required.
