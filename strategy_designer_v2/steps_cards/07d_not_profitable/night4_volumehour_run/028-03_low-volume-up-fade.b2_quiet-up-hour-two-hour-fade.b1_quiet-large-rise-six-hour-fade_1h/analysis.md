---
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5265 USD
---
## Findings
- **F1:** The book loses 0.129 % a day (Sharpe -1.58) while holding the coins earned +0.127 % a day. The idea it trades is too small to cover a trade: per case over 6 hours, the unusual move is +0.02 % (strength 0.009) and the total move is -0.02 %, against a cost of 0.11 % per buy and sell, over 9180 cases.
- **F2:** The trades lose before any fee. BTC's 8310 trades average -0.30 % gross and -0.40 % net, and ETH's 7739 trades average -0.43 % gross and -0.53 % net. Only about 35 % of trades win, and they are held about 9.5 hours.
- **F3:** Larger forecasts do not do better. Trades lose -0.30 %, -0.41 %, -0.28 % and -0.38 % gross across entry-forecast bands 0–3, 3–8, 8–15 and 15–20. The verdict's larger-forecast half also beat the smaller half by -0.026 %, so the grading the idea claims is absent.
- **F4:** Most of the gross loss is being short a coin that drifts up. The book is short on 54 % of bars at a mean position of -0.52. Per bar, the market's own rise costs it -0.17 bp on BTC and -0.16 bp on ETH, while timing adds only +0.05 bp on BTC and -0.07 bp on ETH. Fees add about 0.44 and 0.33 bp per bar on top (turnover 0.080 and 0.060 per bar).
- **F5:** Shorting pays only in a falling month. On bars held short, the gain is +0.23 bp per bar (timing +0.46 bp) in the lowest tercile of the coin's 30-day return. It is -0.74 bp in the middle tercile and -0.57 bp in the top tercile.
- **F6:** The quiet-volume rise fades only when the prior day also rose. The 6-hour short-signed unusual move after quiet rises is +8.7 bp (t 1.31, n 1004) in the top tercile of the 24-hour return. It is -12.0 bp (t -1.85, n 1003) in the bottom tercile.
- **F7:** Large 24-hour moves reverse over the next 24 hours, by more than a trade costs. On a non-overlapping 24-hour grid, the top quintile of the prior 24-hour return (above +2.5 %) is followed by an unusual move of -26.3 bp (t -2.10, n 1072). The bottom quintile (below -2.3 %) is followed by +42.9 bp (t 2.66, n 1072). The middle quintiles show between -11 and +2 bp, with t inside ±1.
- **F8:** The volume split the brief rests on is not in the data either way. After hourly moves beyond 2.5 usual moves, the 6-hour move in the hour's direction is -5.7 bp on volume below 1.5× average (n 2811) and -1.0 bp on volume above 3× (n 3791). At 2 hours the high-volume reading is -10.2 bp, so surging-volume moves do not continue.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade.d1_quiet-spike-after-up-day-fade` (from F1, F5, F6, F7): After an hour in which the coin rises far more than its typical hourly move over the past 30 days while its volume stays near its average hourly volume over the past 30 days, the price gives back part of that rise over the next 24 hours, only while the coin's 24-hour return is also up. The larger that 24-hour rise, the larger the giveback.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade.d2_one-day-move-reverses-next-day` (from F1, F7, F8): Over the next 24 hours a coin moves against its own 24-hour return, and the larger that return in multiples of its usual 24-hour move over the past 30 days, the larger the move back.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade.d3_quiet-rise-fade-in-downtrends` (from F4, F5, F3): While the coin's 30-day return is negative, an hour in which it rises far more than its typical hourly move on near-average volume is followed by a fall over the next 24 hours. The deeper the 30-day decline, the larger that fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
