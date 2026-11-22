---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers
line: 7.g patterns
backtest: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises more than its normal drift over the two hours from 21:00 to 23:00 UTC. The larger the coin's move since 00:00 UTC that day, up or down, the larger that evening rise.
Consequence: A long held from 21:00 to 23:00 UTC is favoured, more so on days that have already moved far, and a short over those hours is refused.
Why:
- F1: The two hours from 21:00 to 23:00 UTC (the close of the bar starting at 20:00 to the close of the bar starting at 22:00) end above the coin's normal 2-hour drift by +0.073 % for BTC (t 4.09) and +0.095 % for ETH (t 4.10), over 2917 non-overlapping days each. In the all-bar hourly table, hour 20 (+0.045 %, t 4.00) and hour 21 (+0.040 %, t 3.69) are the only two of 24 hours above t 3.
- F2: The 21:00–23:00 UTC rise holds across the sample: it is positive in 7 of 8 years (2019 to 2021 and 2023 to 2025 each have t ≥ 2.2; only 2022 is negative, at −0.063 %, t −1.44) and on all 7 weekdays (+0.068 % to +0.107 %).
- F3: The 21:00–23:00 UTC rise is graded by the size of the day's move since 00:00 UTC, in either direction: it is +0.155 % (t 3.42) after the most negative fifth of days so far and +0.121 % (t 3.30) after the most positive fifth, against +0.014 % to +0.069 % for the three middle fifths (1167 days each).
