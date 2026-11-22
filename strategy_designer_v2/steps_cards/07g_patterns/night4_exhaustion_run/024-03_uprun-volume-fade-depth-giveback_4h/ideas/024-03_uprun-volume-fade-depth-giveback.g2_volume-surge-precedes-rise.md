---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback
line: 7.g patterns
backtest: 024-03_uprun-volume-fade-depth-giveback_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The further a coin's 4-hour volume rises above its usual volume over the past 30 days, the more the coin rises over the next 3 days.
Consequence: A volume surge is a reason to hold or take a long and to refuse a short over the following days.
Why:
- F4: A bar whose volume is far above the coin's 30-day median volume (top decile of log volume over its 180-bar median) is followed by an unusual 18-bar move of +0.180 usual moves (t 3.33, 530 cases), against -0.079 (t -2.03) for the lowest-volume decile.
- F3: Among those large 3-day rises (more than 1 usual move), the third with the highest 18-bar volume against its 180-bar median is followed by +0.217 usual moves (t 2.64, 255 cases), against +0.119 (t 1.74) for the lowest-volume third, so rising volume rather than fading volume goes with the larger move up.
