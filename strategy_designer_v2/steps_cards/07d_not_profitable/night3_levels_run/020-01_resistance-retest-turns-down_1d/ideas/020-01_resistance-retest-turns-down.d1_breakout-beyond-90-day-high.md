---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next 5 days.
Consequence: A trader should take a long after a close beyond the 90-day high, larger the further beyond, and refuse a short against such a breakout.
Why:
- F3: Closeness to the 90-day high is followed by rises, not falls. The two grid quintiles nearest the high had 5-day unusual moves of +0.95 % (t 1.97) and +0.60 % (t 1.27), 511 cases each. The middle quintiles were -0.90 % and -0.59 %.
- F4: Closes above the prior 90-day high continue, and more so the further above. In terciles of distance above, the 5-day unusual moves were +0.40 %, +1.11 % and +1.83 %, and the total moves +0.99 %, +1.67 % and +2.47 %. That is 5 to 13 times the 0.19 % cost, but on only 165 cases with t 1.15.
- F6: Breaking a level helps only slightly. Bars where the level above vanished after being present in the prior 5 days were followed by +1.32 % unusual and +1.91 % total over 5 days (155 cases, t 1.24). The move does not grow with the number of earlier turns: +1.81 %, +3.94 %, -2.83 % and +1.46 % by count bin.
- F1: The book lost because it stood short against coins that rose. Its mean position was -0.45 of the book, while the six coins rose 0.07 % to 0.16 % a day on average over all windows. The part of its daily gain owed to the market's own rise was -0.053 %, out of a total of -0.058 %, so timing added almost nothing. Two thirds of the 24 windows lost, and the book's mean daily return was -0.085 %.
