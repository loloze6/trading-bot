---
line: 7.d confirmed, not profitable
backtest: 059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation_1d
idea tested: 059-01.b1.b1.d1.b1.b1.d1_choppy-calm-large-rise-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5044 USD
---
## Findings
- **F1:** The book's failure is a single long fall. Its deepest fall is 40.4 %, running 971 days from w7 to w15, against a yearly return of +9.4 % (Calmar 0.23). Over that stretch the book's daily returns summed to -46 % while the coins' mean summed to +93 %. The fall came mostly from XMR (-1.12), ETH (-0.82), LTC (-0.35) and ADA (-0.24), and it was concentrated in the windows where the coins fell: w7, w9, w12 and w14, with trade sums of -230, -279, -81 and -477 points.
- **F2:** The cases the idea itself calls give-backs are traded anyway. Because the forecast is standardised against its own past 60 values, weeks with a raw scaled rise of 0.5 usual weekly swings or less still received a positive forecast. On the grid inside the profile those 13 cases returned -15.1 % against the coin's drift over 14 days (t -3.29). Cases with a raw scaled rise above 1.5 returned +13.6 % (t 2.50, n 12), and the middle bands returned +11.2 % and +37.6 %. The lowest forecast tercile lost -13.7 % (t -3.04), and its mean raw scaled rise was only 0.23.
- **F3:** The effect grows with the horizon. For raw scaled rises above 1.5, the excess return over 28 days is +27.4 % (t 4.63, n 9), against +13.6 % over 14 days. Over all profile signals it is +14.4 % over 28 days (t 1.76, n 33), against +6.6 % over 14 days (t 1.21, n 42). The top forecast tercile earns +32.2 % over 28 days (t 3.12, n 11).
- **F4:** A strong rise that closes near the coin's 30-day high carries the gain. Signals with a raw scaled rise above 0.5 and a close within 3 % of the 30-day high earned +20.7 % excess over 14 days (t 2.00, n 18), against +13.4 % (n 7) below the high. In trades, entries near the high netted +10.8 % per trade (median +2.1 %, n 105), against +1.4 % (median +0.1 %, n 174) below it. Being near the high is not an effect of its own: near-high bars without the signal returned -4.6 % over 14 days (t -1.90, n 75) and -6.7 % over 28 days (t -1.76, n 63). It fits the theory's "move leaves the range" step.
- **F5:** Signals in the upper half of the choppy band do better. Signals with a positive 60-day return earned +14.6 % excess over 14 days (n 17), against +1.1 % (n 25) when the 60-day return was negative. Trades entered after a positive 30-day return netted +9.9 % (median +2.4 %, n 136), against +0.2 % (median -0.2 %, n 143). The condition alone does not earn: in-profile bars without the signal and with a positive 60-day return returned -8.3 % (n 7). These samples are small.
- **F6:** Near the high does not protect the book in the losing windows. In w7, w9, w12 and w14, trades lost in every raw-scaled-rise band, from -4.6 % to -11.3 % net. Trades near the high lost -7.8 %, and those below it lost -8.3 %. The 28-day forward return after entries in those windows was -13 % to -21 %. These falls were market-wide declines that no single coin's state flagged.

## Ideas
- `059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks` (from F2, F3, F1): In a choppy, calm market, the larger a coin's rise over the past 7 days in multiples of its usual 7-day swing over the past 30 days, the larger its further rise over the next 28 days. The size of the move is read from that raw multiple itself, so a rise of only a fraction of a usual week gives back over the same 28 days.
- `059-01.b1.b1.d1.b1.b1.d1.d2_range-break-rise-continues` (from F4, F2, F1): In a choppy, calm market, the larger a coin's rise over the past 7 days in multiples of its usual 7-day swing over the past 30 days, and the closer its close sits to its highest close of the past 30 days, the larger its further rise over the next 14 days.
- `059-01.b1.b1.d1.b1.b1.d1.d3_rise-continues-in-upper-chop` (from F5, F1, F2): In a choppy, calm market, the larger a coin's rise over the past 7 days in multiples of its usual 7-day swing over the past 30 days, and the higher its 60-day return within the choppy band, the larger its further rise over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
