---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits below its highest close of the past 90 days, the more it rises over the next 5 days.
Consequence: A trader should read nearness to the recent high as a reason to be long, not as a ceiling to short.
Why:
- F3: Closeness to the 90-day high is followed by rises, not falls. The two grid quintiles nearest the high had 5-day unusual moves of +0.95 % (t 1.97) and +0.60 % (t 1.27), 511 cases each. The middle quintiles were -0.90 % and -0.59 %.
- F2: The resistance effect is not in these bars. The verdict's unusual move was -0.05 % per case over 5 days, a strength of 0.002 against a usual move of 10.6 %, or -0.2 times the 0.19 % cost of a trade. The Spearman correlation between the count of turns above and the 5-day unusual move is 0.009. Unusual moves across count bins from 0–1 to 5 or more show no gradient (-0.12 %, +0.11 %, +0.78 %, -0.93 %).
- F1: The book lost because it stood short against coins that rose. Its mean position was -0.45 of the book, while the six coins rose 0.07 % to 0.16 % a day on average over all windows. The part of its daily gain owed to the market's own rise was -0.053 %, out of a total of -0.058 %, so timing added almost nothing. Two thirds of the 24 windows lost, and the book's mean daily return was -0.085 %.
