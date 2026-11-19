---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.d not profitable
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The stronger a coin's 10-day return relative to its own 20-day volatility, the more its price rises over the next 3 days relative to its usual 3-day return, with the extra rise concentrated after the strongest advances, and the larger the more its last 1-day return has fallen.
Consequence: A strong 10-day advance followed by a falling last day is the moment to add long, while one that keeps grinding up over the last day is no reason to add.
Why:
- F3: On heavy long bars (position above 0.5, 91,889 bars), the gain per bar was 0.000270 (t 3.27) when the close stood furthest below its 240-hour high (mean -10.5%). It was only 0.000034 to 0.000062 (t 0.52 to 0.79) in the two quintiles nearest that high (mean -1.9% and -0.7%), and those are where the position was largest (1.09 to 1.11).
- F4: On the same heavy bars, the gain was 0.000297 per bar (t 4.64) when the last 24 hours had fallen (mean ret24 -3.2%). It was -0.000008 (t -0.15) after a flat-to-small rise (mean +1.2%).
- F1: The book's deepest fall was -53.5%, running from w1 to w10 (1127 days); over that stretch the book's daily returns summed to -0.67 against -0.52 for holding, so it lost more than the coins it followed. That fall alone sets the Calmar of 0.23.
