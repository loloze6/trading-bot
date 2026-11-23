---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3926 USD
---
## Findings
- **F1:** The tested forecast sorts the coming 5-day move the way the idea says, but weakly. The top forecast quintile is followed by an excess 5-day return of +0.75 % (t 2.03, 952 cases) and the second-lowest quintile by −0.61 % (t −1.81, 943 cases). The lowest quintile shows only −0.21 % (t −0.53), so the effect is not graded at the extreme short end.
- **F2:** The forecast's signed excess gain is positive in all 8 years, from 2018 to 2025, at +0.19 % to +0.90 % per 5-day case, but no single year reaches t 1.4 (largest t 1.39 in 2021, 474 cases). The idea's small edge is steady, not carried by one period.
- **F3:** Long and short forecasts earn about equally. Long cases are followed by an excess +0.37 % (t 1.72, 2457 cases) and short cases by −0.40 % (t −1.74, 2275 cases), so the book's edge is not a long bias.
- **F4:** On the 5-day grid, the past 5-day return reverses only in high volatility. Its Spearman correlation with the next 5-day excess return is −0.085 in the top volatility third (1312 cases), −0.034 in the middle third and +0.027 in the bottom third. The cases are pooled over coins on shared dates, so the high-volatility value (a naive t near −3) is overstated.
- **F5:** Sorted by past 5-day, 20-day return or nearness to the 60-day high, no quintile pattern is monotone.
- **F6:** Saturday is the only weekday whose daily excess return survives averaging across coins per date: +0.37 % (t 2.43, 414 days; pooled t 4.47). It is positive in 7 of 8 years and has a positive t in 14 of 15 coins. It is also the quietest day, with a mean absolute return of 2.39 % against 3.2–3.6 % on weekdays.
- **F7:** The other weekday effects lose their weight once coins are averaged per date (all |t| ≤ 1.51 date-clustered).
- **F8:** The book's daily return rises with the coin's own daily return, from −0.08 % in the second decile of coin days to +0.20 % in the ninth. Its value moves with the market's daily swings despite the balanced long and short counts in F3.
- **F9:** The idea's move is too small next to a trade. Per 5-day case the total move is +0.14 % and the unusual move +0.15 %, against a cost of 0.22 % per trade (0.6 and 0.7 times the cost). Its strength is 0.015, about a third of the 0.05 seen in real ideas.

## Ideas
- No ideas: Across about twelve angles and over 60 groupings, nothing stands out from chance once coins sharing dates are accounted for. The Saturday drift (F6, t 2.43) is a calendar condition, not a graded effect. The high-volatility 5-day reversal (F4) rests on a correlation that pooling over shared dates inflates, so neither supports a graded idea of its own.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
