---
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses_1d
idea tested: 003-01_thin-volume-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3425 USD
---
## Findings
- **F1:** The book's fees are larger than everything its timing earns. Its 4297 trades are all shorts, held about 1.67 days on average, and they lose -0.54% each after fees. Per bar, fees cost 0.000303 against a timing gain of 0.000264. Summed over all bars, fees come to 5.32 against timing of 4.58.
- **F2:** Being short a rising market costs the book on top of the fees. It is short on 29.6% of bars with a mean allocation of -0.186, and the coins' own rise takes -0.000219 per bar from it. Every coin's mean daily return is positive (0.00067 to 0.00155) while the book's ranges from -0.000502 to +0.000058.
- **F3:** Thin-volume rises are not followed by any giveback. On the 999 active grid cases, the main measure's mean is -0.0014 (t -0.30). By rise-size quartile, the excess 5-day return runs +0.0081, -0.0075, -0.0079, +0.0060, with no |t| above 1.25. Among thin-volume rises, the largest third shows +0.0009 (t 0.12, n 150).
- **F4:** The short pays only when the coin is already in a 20-day decline. There, held short bars gain 0.000702 per bar (timing 0.00145, t 1.42, n 3018), against -0.000632 (t -1.11, n 2168) when the 20-day return is up. Active cases show the same split: excess 5-day return -0.0058 (t -1.42, n 618) in 20-day declines versus +0.0047 (t 0.82, n 381) in 20-day rises.
- **F5:** The effect actually in the data runs the other way, on heavy volume. Rises on above-average volume are followed by excess 5-day returns that grow with the rise's size: -0.0030 (t -0.36) for the smallest third, +0.0125 (t 1.44) for the middle third and +0.0282 (t 2.79, n 169) for the largest third. The largest third of all up days on above-average volume shows +0.0248 (t 3.51, n 305).
- **F6:** Sharp falls on thin volume keep falling rather than reverting. The largest third of thin-volume down days shows an excess 5-day return of -0.0159 (t -2.43, n 174), against +0.0053 (t 1.03, n 318) for the largest falls on heavy volume.

## Ideas
- `003-01_thin-volume-rise-reverses.d1_thin-rise-fades-in-downtrends` (from F2, F3, F4): When a coin rises sharply over one day on volume well below its own 30-day average daily volume, it gives back part of that rise over the next 5 days, only while the coin's 20-day return is negative. The larger the rise, the thinner its volume against that average, and the deeper the 20-day decline, the larger the giveback.
- `003-01_thin-volume-rise-reverses.d2_heavy-volume-rise-continues` (from F1, F2, F5): When a coin rises sharply over one day on volume above its own 30-day average daily volume, it keeps rising over the next 5 days, by more than its usual 5-day return. The larger the day's rise against its 20-day volatility, the larger the further gain.
- `003-01_thin-volume-rise-reverses.d3_thin-volume-fall-continues` (from F6): When a coin falls sharply over one day on volume well below its own 30-day average daily volume, it keeps falling over the next 5 days. The larger the fall against its 20-day volatility, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
