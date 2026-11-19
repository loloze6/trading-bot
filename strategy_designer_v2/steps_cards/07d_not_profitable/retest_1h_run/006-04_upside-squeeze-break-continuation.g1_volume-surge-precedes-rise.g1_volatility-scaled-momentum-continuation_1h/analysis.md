---
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
idea tested: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3884 USD
---
## Findings
- **F1:** The book's deepest fall was -53.5%, running from w1 to w10 (1127 days); over that stretch the book's daily returns summed to -0.67 against -0.52 for holding, so it lost more than the coins it followed. That fall alone sets the Calmar of 0.23.
- **F2:** Inside the fall the book lost even where the coins rose. In w6 the book made -0.146 while holding made +0.273, and in the w10 part it made -0.126 against +0.079. By coin, XMR lost -1.72 and ZEC -1.86 against holding's -0.18 and -1.32.
- **F3:** On heavy long bars (position above 0.5, 91,889 bars), the gain per bar was 0.000270 (t 3.27) when the close stood furthest below its 240-hour high (mean -10.5%). It was only 0.000034 to 0.000062 (t 0.52 to 0.79) in the two quintiles nearest that high (mean -1.9% and -0.7%), and those are where the position was largest (1.09 to 1.11).
- **F4:** On the same heavy bars, the gain was 0.000297 per bar (t 4.64) when the last 24 hours had fallen (mean ret24 -3.2%). It was -0.000008 (t -0.15) after a flat-to-small rise (mean +1.2%).
- **F5:** Fees ate about half of the gross gain: 0.000019 against 0.000039 per bar, over 32,526 trades (1.83 per day, median 9 hours). In the transitional forecast quintile (mean forecast 7.3), fees of 0.000088 per bar exceeded that quintile's gain of 0.000027.
- **F6:** Only the full-cap forecast quintile (forecast 20, position 1.00) earned clearly: 0.000185 per bar, coin r1 t 4.19. The book's mean daily return of 0.00043 was below holding's 0.00118 at a mean position of 0.27, and its timing part (0.000023 per bar) was about as large as its market part (0.000016).
- **F7:** On the 72-hour grid among forecast>0 cases, the excess return was 0.0102 (t 2.65, n=587) when 24-hour volatility stood highest against 480-hour volatility (ratio 1.46). The middle quartiles showed -0.0052 (t -1.63) and 0.0005.

## Ideas
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.d1_buy-pullbacks-in-advances` (from F1, F2, F3, F6): The stronger a coin's 10-day return relative to its own 20-day volatility, the more its price rises over the next 3 days relative to its usual 3-day return, with the extra rise concentrated after the strongest advances, and the larger still the further its close has pulled back below its highest price of the last 10 days.
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.d2_advance-with-one-day-dip` (from F3, F4, F1): The stronger a coin's 10-day return relative to its own 20-day volatility, the more its price rises over the next 3 days relative to its usual 3-day return, with the extra rise concentrated after the strongest advances, and the larger the more its last 1-day return has fallen.
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.d3_persistent-volatility-scaled-advance` (from F5, F6): The longer a coin's 10-day return relative to its own 20-day volatility has stayed strong over the past 3 days, the more its price rises over the next 3 days relative to its usual 3-day return.
- `006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation.d4_advance-with-awakening-volatility` (from F7, F6): The stronger a coin's 10-day return relative to its own 20-day volatility, the more its price rises over the next 3 days relative to its usual 3-day return, with the extra rise concentrated after the strongest advances, and the larger the higher its last 1-day volatility stands against its own 20-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
