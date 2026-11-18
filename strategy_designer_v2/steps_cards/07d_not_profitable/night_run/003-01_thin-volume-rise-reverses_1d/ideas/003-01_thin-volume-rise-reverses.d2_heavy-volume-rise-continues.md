---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume above its own 30-day average daily volume, it keeps rising over the next 5 days, by more than its usual 5-day return. The larger the day's rise against its 20-day volatility, the larger the further gain.
Consequence: A trader would go long after large heavy-volume up days rather than short, which puts the drift that cost the tested book on the trader's side.
Why:
- F1: The book's fees are larger than everything its timing earns. Its 4297 trades are all shorts, held about 1.67 days on average, and they lose -0.54% each after fees. Per bar, fees cost 0.000303 against a timing gain of 0.000264. Summed over all bars, fees come to 5.32 against timing of 4.58.
- F2: Being short a rising market costs the book on top of the fees. It is short on 29.6% of bars with a mean allocation of -0.186, and the coins' own rise takes -0.000219 per bar from it. Every coin's mean daily return is positive (0.00067 to 0.00155) while the book's ranges from -0.000502 to +0.000058.
- F5: The effect actually in the data runs the other way, on heavy volume. Rises on above-average volume are followed by excess 5-day returns that grow with the rise's size: -0.0030 (t -0.36) for the smallest third, +0.0125 (t 1.44) for the middle third and +0.0282 (t 2.79, n 169) for the largest third. The largest third of all up days on above-average volume shows +0.0248 (t 3.51, n 305).
