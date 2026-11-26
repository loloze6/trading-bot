---
line: 7.g patterns
backtest: 060-01_falling-agitated-high-close-fade_1d
idea tested: 060-01_falling-agitated-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3704 USD
---
## Findings
- **F1:** The tested idea is not graded the way it claims. Inside the strategy's regime, closes in the top fifth of the day's range (location 0.6 to 1) were followed by a next-day excess of +0.08 % over 59 bars, which is no fade. Mid-upper closes (0.2 to 0.6) were followed by −0.92 % over 82 bars, and on held bars the gain was −0.31 % in the top bucket against +0.26 % in the 0.2 to 0.6 bucket.
- **F2:** Across all bars, the next-day excess does not fall steadily as the close nears the high. It is −0.61 % (t −2.09, 539 bars) for closes at 0.2 to 0.6 and −0.11 % (t −0.40, 508 bars) for closes at 0.6 to 1. The single bucket at t −2 stands among about 40 groupings looked at, so it does not stand out from chance.
- **F3:** The clearest pattern is a next-day rebound after the weakest days. The lowest quintile of the day's return was followed by +0.163 usual moves (t 3.05, 480 bars). In bars the detector placed in the falling-agitated profile, that excess was +1.88 % (t 2.67, cases of one day summed, 93 cases on 72 days). The profile map already holds this effect with 16 long strategies in falling agitated (038-01, 047-01, 051-01 and others), so it is not a discovery.
- **F4:** Down days that close in the upper third of their range were followed by −1.72 % next day (t −1.86, 96 cases on 86 days) and −2.67 % over two days (t −1.72, 46 cases). Inside the profile they leave only 14 cases. The grading is absent: the Spearman correlation of close location with the next-day move on down days is −0.038, and of the lower-wick share −0.039.
- **F5:** No weekday, volatility quintile, 5-day or 20-day return quintile, or relative-range quintile showed a next-day effect with |t| above 2.1, from 7 weekdays and 5 quintiles of each measure.
- **F6:** The book's losses sit in a few places. BCH trades lost 2.44 % on average after fees (31 trades) and ZEC trades 0.60 % (111 trades). Window w13 alone summed −21 % of daily book return against at most +8 % in any other window. The size, +0.36 % unusual move with t 1.33, is about 1.1 times the 0.32 % cost of a trade.

## Ideas
- No ideas: The only pattern that clears chance after this many angles is the next-day rebound after the weakest days in falling agitated markets (F3), which the profile map already holds with 16 strategies; the tested idea's own fade is not graded (F1, F2), and the down-day high-close fade (F4) is too thin and ungraded to stand out.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
