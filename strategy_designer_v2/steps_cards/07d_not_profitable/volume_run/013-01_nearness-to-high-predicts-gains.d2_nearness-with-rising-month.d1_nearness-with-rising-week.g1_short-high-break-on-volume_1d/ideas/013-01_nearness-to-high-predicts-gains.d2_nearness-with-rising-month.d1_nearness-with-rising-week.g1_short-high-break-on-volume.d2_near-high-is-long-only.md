---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 20 days, and the heavier that day's volume against its 30-day average, the larger the coin's rise over the next 7 days, the move being an absolute gain that grows with closeness and volume, while closes far below the high on thin volume are followed by smaller rises rather than falls.
Consequence: Read the signal as a long-only scale from flat to a full long, never taking a short when the close sits deep below the high.
Why:
- F1: The book's whole gain comes from its long side. Long bars summed +6.32 in gain before fees against 1.13 in fees. Short bars summed −0.36 before fees and paid another 0.79 in fees, so after fees the shorts are a net loss of about 1.14 over 8,517 bars.
- F2: Removing the shorts repairs the failing Calmar but not the mean. A long-only version of the same book has mean daily return 0.000296 against 0.000229, Sharpe 1.02 against 0.61, deepest fall −13.3% against −19.8%, and Calmar 0.81 against 0.39 (the rule needs 0.75).
- F3: The lowest forecast quintile does not lead to falling coins. It sits 1.07% below the coin's 7-day mean, yet its raw 7-day return is −0.14%, and the bars held short rose on average (+0.0068% a day). The deep-below, thin-volume side forecasts relative weakness, not an absolute fall.
- F5: Shorts lose most where the coin trends hardest. In the top 60-day-return quartile (+79% on average) shorts lose −0.029% a day, and in the bottom quartile (−36%) they lose −0.021% a day. Shorts gain only in the mildly falling quartile (+0.062%).
