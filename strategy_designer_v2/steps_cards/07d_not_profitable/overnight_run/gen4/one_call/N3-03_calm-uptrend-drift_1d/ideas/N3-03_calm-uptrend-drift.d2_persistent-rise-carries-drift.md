---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-03_calm-uptrend-drift
line: 7.d not profitable
backtest: N3-03_calm-uptrend-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The upward drift after a calm rise belongs to coins whose 20-day return has stayed positive for several consecutive weeks; a coin whose 20-day return has only just turned positive gives back the rise within the next few days.
Consequence: A trader would enter only once the positive 20-day return has persisted, and would refuse fresh turns that tend to end in quick losing exits.
Why:
- F3: Short holds lose and long holds pay: trades held 1.5 days or less made a mean −2.04% before fees (n 534), those held 1.5 to 3.5 days −1.29% (n 559), those held 3.5 to 7.5 days −0.17% (n 548), against +3.03% for 7.5 to 15.5 days (n 392) and +10.5% beyond 15.5 days (n 291); the 1101 trades held 3.5 days or less summed −1812% before fees, against +4147% for the 1231 longer ones, with an overall win rate of only 39%.
- F4: A larger forecast earns only weakly more: non-overlapping 5-bar forward returns were +1.12% when the forecast was above 2.5 (n 721, t 2.74) against +0.41% on flat bars (n 2522, t 1.85), with no ordering among the small middle buckets (n 29 to 69, means −1.7% to +2.4%); by entry forecast, trades entered above 5 made +1.00% (n 1919) and those entered between 2.5 and 5 made +1.34% (n 336).
- F5: Inside the active set, the size of the 20-day rise and the calm do not grade the gain: by 20-day-return tercile the 5-bar forward return was +0.39%, +2.04% and +0.76% (n about 255 each); by 20-day-volatility tercile it was +0.57% for the calmest third against +2.03% for the most volatile third.
