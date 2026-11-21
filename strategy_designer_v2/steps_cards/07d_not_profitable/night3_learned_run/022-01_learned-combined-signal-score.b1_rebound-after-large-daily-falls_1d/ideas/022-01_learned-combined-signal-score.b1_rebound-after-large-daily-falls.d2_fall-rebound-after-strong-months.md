---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls
line: 7.d not profitable
backtest: 022-01_learned-combined-signal-score.b1_rebound-after-large-daily-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall compared with its 30-day volatility, the higher its return over the next 1 day, the more so the larger the size of its 30-day return, whether that return was a rise or a fall.
Consequence: A trader would buy large daily falls after a month that moved strongly, up or down, and refuse falls that come after a flat month.
Why:
- F3: The losing bars are the falls that come without a volatility burst. Bars with a low 7-day against 30-day volatility and a middling 30-day return have a next-day excess of -0.47 % (t -3.49, 734 bars). Bars with a high ratio gain in every 30-day state: +0.88 % (t 3.49) when the 30-day return is low, +0.23 % when it is middling, +0.64 % (t 3.46) when it is high.
- F5: The rebound is larger after the coin has already moved far over the month, in either direction. By the coin's 30-day return, the next-day excess is +0.45 % (t 3.18) in the lowest quarter and +0.35 % (t 2.76) in the highest, against +0.00 % and -0.11 % in the two middle quarters. The 7-day return shows the same U-shape: +0.37 % and +0.54 % at its ends, -0.17 % and -0.04 % in its middle.
