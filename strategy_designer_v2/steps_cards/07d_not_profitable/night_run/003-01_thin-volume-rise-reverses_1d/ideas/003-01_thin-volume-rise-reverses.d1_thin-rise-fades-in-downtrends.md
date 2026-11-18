---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well below its own 30-day average daily volume, it gives back part of that rise over the next 5 days, only while the coin's 20-day return is negative. The larger the rise, the thinner its volume against that average, and the deeper the 20-day decline, the larger the giveback.
Consequence: A trader would short thin-volume rises only inside a falling market, and would refuse them in a rising one, where the short only fights the coin's drift and pays fees.
Why:
- F2: Being short a rising market costs the book on top of the fees. It is short on 29.6% of bars with a mean allocation of -0.186, and the coins' own rise takes -0.000219 per bar from it. Every coin's mean daily return is positive (0.00067 to 0.00155) while the book's ranges from -0.000502 to +0.000058.
- F3: Thin-volume rises are not followed by any giveback. On the 999 active grid cases, the main measure's mean is -0.0014 (t -0.30). By rise-size quartile, the excess 5-day return runs +0.0081, -0.0075, -0.0079, +0.0060, with no |t| above 1.25. Among thin-volume rises, the largest third shows +0.0009 (t 0.12, n 150).
- F4: The short pays only when the coin is already in a 20-day decline. There, held short bars gain 0.000702 per bar (timing 0.00145, t 1.42, n 3018), against -0.000632 (t -1.11, n 2168) when the 20-day return is up. Active cases show the same split: excess 5-day return -0.0058 (t -1.42, n 618) in 20-day declines versus +0.0047 (t 0.82, n 381) in 20-day rises.
