---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume well below its own 30-day average daily volume, it gives back part of that rise over the next day. The giveback grows the further below that average the volume lies, and it is largest for the sharpest rises on the very thinnest volume.
Consequence: A trader would size the short by how extreme the thinness is, keeping it for rises on the very thinnest volume, where the giveback shows, and not for rises on only modestly thin volume, which carry on.
Why:
- F1: The book's gain is lost in the moderately thin band (volume 0.5 to 0.75 of its 30-day average, regime chop): its 854 signal bars average -0.001019 per bar and its 682 trades average -1.51 % after fees, while the very-thin band (0.5 or less, regime mean_reversion) earns +0.000891 per bar on 955 signal bars and -0.44 % per trade.
- F2: Inside the very-thin band the giveback is graded the way the idea says: next-day excess return is -0.0036 for forecasts of 8 to 15 (111 bars) and -0.0064 for 15 to 20 (191 bars). In the moderately thin band the same forecast sizes are followed by rises, +0.0034 (121 bars) and +0.0041 (104 bars), so the larger short there loses more.
