---
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3966 USD
---
## Findings
- **F1:** The signal's gain comes only from days that closed lower than the day before. Signal bars on down days were followed by a next-day return of +0.52 % (3678 bars). Signal bars on up days were followed by −0.21 % (3791 bars). The coin alone on non-signal days earned +0.08 % on down days (4795 bars) and +0.08 % on up days (4972 bars). So a down day by itself carries no effect, and the gain is the idea's signal on a down day.
- **F2:** Letting the existing book trade only when the signal's day closed lower fixes the measure that failed. The rebuilt book, with the backtest's costs, matched the actual one closely (Calmar 0.657 rebuilt against 0.647 recorded). Restricted to down days it reaches a Calmar of 1.24 against 0.66, a deepest fall of −21.2 % against −31.2 %, a yearly return of +26.3 % against +20.5 % and a Sharpe of 1.13 against 0.80, while in a position on 25 % of coin-days instead of 50 %.
- **F3:** The effect is graded by the size of the day's fall measured in the coin's 20-day volatility (the day's return over the standard deviation of its last 20 daily returns).
- **F4:** Inside signal days that closed lower, the effect also rises with the forecast. The top half of the forecast (mean forecast 18.8, 1839 bars) was followed by +1.02 %, against +0.13 % and −0.06 % in the two lower quarters (920 and 919 bars).
- **F5:** The book's six deepest falls all came while the coins' average was falling hard. The coins fell 79 % during the −31 % fall in w12–w14, 67 % during the −24 % fall in w1–w3, and 48 % during the −27 % fall in w16–w17. The losses came from long positions taken after up-day signals: when price was below its 100-day mean, signal bars on up days were followed by −0.41 % (819 bars), against +0.02 % for the same bars without the signal. Signal bars on down days still earned +0.67 % in that same falling state (918 bars).
- **F6:** Neither a trend filter nor the volatility regime explains the failure.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d1_absorbed-selling-on-down-days` (from F1, F2, F3, F5): The heavier a coin's volume on a day relative to its own prior 20-day average, and the lower the day's close sits within its high-low range, the more the coin rises over the next day, while its 20-day volatility is high against its history. This holds when the day itself closed lower than the day before, and the rise is larger the larger that day's fall is against the coin's 20-day volatility.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.d2_strong-absorption-down-days-any-trend` (from F1, F4, F5, F6): The heavier a coin's volume on a day relative to its own prior 20-day average, and the lower the day's close sits within its high-low range, the more the coin rises over the next day, while its 20-day volatility is high against its history. This holds on days that closed lower than the day before, including while the coin's price is below its own 100-day average, and the rise grows with the strength of the volume and close-location signal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
