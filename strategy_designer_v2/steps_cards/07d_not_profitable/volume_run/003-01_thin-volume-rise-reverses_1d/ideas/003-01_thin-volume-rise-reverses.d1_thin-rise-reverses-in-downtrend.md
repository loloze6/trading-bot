---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well below its own 30-day average daily volume, it gives back part of that rise over the next 5 days, only while the coin has fallen over the past 30 days. The larger the rise, the thinner its volume against that average and the deeper the 30-day fall, the larger the giveback.
Consequence: A trader would short thin-volume one-day rises only inside a 30-day decline and refuse them while the coin is rising, which removes the short-against-the-trend losses of rising years.
Why:
- F3: Signal bars that come after a 30-day fall of more than 10 % are followed by a next-day excess return of -0.0043 (t -2.74, 942 bars). After flat or rising 30-day returns it is near zero: +0.0005 (563), -0.0009 (551) and -0.0003 (865).
- F4: The book earns in falling years and loses in rising ones: per-active-bar gain is +0.00042, +0.00076 and +0.00091 in 2018, 2019 and 2022 (coin next-day means -0.0043, -0.0018, -0.0040), against -0.00063, -0.00173 and -0.00068 in 2020, 2021 and 2025 (coin means +0.0043, +0.0048, +0.0050).
- F5: Being short against the coins' rise (coin daily mean +0.00119) costs -0.000042 per bar. Timing adds only +0.000024 and fees take 0.000069 per bar, which leaves a mean daily book return of -0.0000885 and a Sharpe of -0.58.
