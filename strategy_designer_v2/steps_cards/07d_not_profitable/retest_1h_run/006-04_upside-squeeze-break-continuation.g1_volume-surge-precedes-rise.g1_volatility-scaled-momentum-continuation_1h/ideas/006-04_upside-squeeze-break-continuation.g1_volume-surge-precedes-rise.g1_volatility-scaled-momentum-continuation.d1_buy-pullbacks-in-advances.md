---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The stronger a coin's 10-day return relative to its own 20-day volatility, the more its price rises over the next 3 days relative to its usual 3-day return, with the extra rise concentrated after the strongest advances, and the larger still the further its close has pulled back below its highest price of the last 10 days.
Consequence: Within a strong volatility-scaled advance, a trader should lean long harder into the pullback and lighten the position as the price presses against its fresh 10-day high, where the falls came from.
Why:
- F1: The book's deepest fall was -53.5%, running from w1 to w10 (1127 days); over that stretch the book's daily returns summed to -0.67 against -0.52 for holding, so it lost more than the coins it followed. That fall alone sets the Calmar of 0.23.
- F2: Inside the fall the book lost even where the coins rose. In w6 the book made -0.146 while holding made +0.273, and in the w10 part it made -0.126 against +0.079. By coin, XMR lost -1.72 and ZEC -1.86 against holding's -0.18 and -1.32.
- F3: On heavy long bars (position above 0.5, 91,889 bars), the gain per bar was 0.000270 (t 3.27) when the close stood furthest below its 240-hour high (mean -10.5%). It was only 0.000034 to 0.000062 (t 0.52 to 0.79) in the two quintiles nearest that high (mean -1.9% and -0.7%), and those are where the position was largest (1.09 to 1.11).
- F6: Only the full-cap forecast quintile (forecast 20, position 1.00) earned clearly: 0.000185 per bar, coin r1 t 4.19. The book's mean daily return of 0.00043 was below holding's 0.00118 at a mean position of 0.27, and its timing part (0.000023 per bar) was about as large as its market part (0.000016).
