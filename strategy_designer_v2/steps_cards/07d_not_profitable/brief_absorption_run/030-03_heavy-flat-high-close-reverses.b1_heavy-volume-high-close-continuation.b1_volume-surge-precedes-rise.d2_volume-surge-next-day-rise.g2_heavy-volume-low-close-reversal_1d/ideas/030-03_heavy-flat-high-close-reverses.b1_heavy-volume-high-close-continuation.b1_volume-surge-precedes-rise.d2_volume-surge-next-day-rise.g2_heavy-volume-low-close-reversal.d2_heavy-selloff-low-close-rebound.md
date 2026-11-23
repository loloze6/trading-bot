---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g2_heavy-volume-low-close-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day whose volume is heavy against the coin's prior 20-day average and whose return fell well below the coin's prior 20-day volatility, the lower the close sits within that day's high-low range, the more the coin rises over the next day, and the larger the day's fall against that volatility, the larger the rise.
Consequence: A trader goes long for one day on a heavy-volume selloff that closed near its low, and does not treat a flat or rising heavy-volume day closing low as a reason to be long.
Why:
- F4: The effect lives on days that fell hard. On days down more than one prior 20-day standard deviation, signals earn +0.59 % excess next day (1622 cases), while the same down days without the signal earn −0.05 % (172 cases), so the down day alone is not the effect. Removing these down days from the book collapses it (Calmar 0.008, Sharpe 0.14). On days with |z| < 0.3, signals earn only +0.13 % (978 cases).
- F2: The size of the move is the binding limit. The total move per case is +0.23 % against a 0.19 % cost per trade, 1.2 times the cost, and the unusual move of +0.11 % is 0.6 times the cost (strength 0.025). Only a stronger case of the situation can carry the fees.
- F5: In the book's falls (days more than 15 % under its peak, 718 of 2898 days), signals earn −0.40 % excess next day (1516 cases), against +0.50 % outside them (4602 cases). The signal days inside the falls had a 20-day return of −7.6 % (against +4.9 % outside) and sat below their 50-day mean 80 % of the time (against 43 %). The falls come from signals taken inside the coin's own sustained declines.
