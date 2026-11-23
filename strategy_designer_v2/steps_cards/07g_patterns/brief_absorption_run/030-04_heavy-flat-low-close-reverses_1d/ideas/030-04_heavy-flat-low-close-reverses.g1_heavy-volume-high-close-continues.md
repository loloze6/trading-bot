---
brief: 030_absorption-day-close-location
source-idea: 030-04_heavy-flat-low-close-reverses
line: 7.g patterns
backtest: 030-04_heavy-flat-low-close-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's high, the more the coin rises over the next 5 days.
Consequence: A heavy-volume day that closes near its high is a reason to be long the coin for about a week and to refuse a short on it, the opposite of the tested reversal.
Why:
- F1: On heavy-volume days (volume at least 2× the prior 20-day mean, first per 5-day grid cell), a close in the upper third of the range was followed by a 5-day excess move of +0.149 usual moves (t 2.56, n 341), or +1.76 % excess and +2.38 % total (t 3.47), well above the 0.19 % cost of a trade. Heavy days closing mid-range gave −0.007 (t −0.10, n 246), and heavy days closing in the lower third gave +0.045 (t 0.72, n 253).
- F2: The upper-close effect belongs to heavy volume: on ordinary-volume days (volume below 1.5× its mean), an upper-third close gave only +0.026 usual moves (t 0.86, n 951).
- F4: The upper-close effect after heavy days is positive on all 6 coins (from +0.048 on LTC to +0.224 on ZEC, ZEC t 2.03) but unstable across years: +0.587 (t 4.12) in 2024 and +0.491 (t 2.43) in 2020, against −0.304 (t −1.80) in 2018 and −0.185 (t −1.52) in 2022.
- F5: The tested book lost because it shorted exactly these days. Its 427 short trades lost −4.45 % each after fees (t −6.66, 23 % winners), on every coin except XMR (+0.07 %) and in every year from 2019. Its 308 long trades earned +2.31 % (t 3.25), and the book's daily mean is within ±0.03 % of zero on every coin.
