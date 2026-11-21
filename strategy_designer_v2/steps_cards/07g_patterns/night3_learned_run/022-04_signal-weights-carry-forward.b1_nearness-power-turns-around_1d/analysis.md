---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3541 USD
---
## Findings
- **F1:** The book's gain is timing, not the market's rise. Its mean daily return is 0.060 %, of which only 0.0095 % comes from the position held times the coin's mean daily return. The mean position is +0.054 against a mean absolute position of 0.39.
- **F2:** The forecast's gain comes from its long side. With forecast/10 times the 5-day excess return, long cells earn +0.72 % (t 2.17, 1565 cases) and short cells +0.20 % (t 0.63, 1453 cases).
- **F3:** Five of six coins confirm the forecast and ZEC does not. ZEC's Spearman of forecast against the 5-day excess return is −0.002 and its forecast gain −0.43 % (t −0.57, 452 cases), against +0.04 to +0.08 and +0.31 % to +0.88 % on the other five.
- **F4:** The book's fall that fails the Calmar test is concentrated in a few windows. The deepest is −25 % in w14, then −19 % in w16 and −18 % in w2; across all years the forecast gain ranges from −0.26 % in 2018 to +1.37 % in 2021, and no year reaches t 2.
- **F5:** The book rises with the coins' day but only weakly. Its daily return goes from −0.08 % on the coins' worst-quintile days (coins −5.3 %) to +0.27 % on their best-quintile days (coins +5.3 %), with a correlation of 0.12 over 2898 days.
- **F6:** Coins do somewhat better after a large up day, but not reliably. Over 5 days after a top-quintile day (return over 20-day volatility), the excess return is +1.46 % (t 2.66, 502 cases). The pattern is not graded: the Spearman over all days is −0.006, and the fourth quintile shows −0.67 %. It splits by coin: BTC t 2.07, XRP 1.75, ZEC 1.81, LTC −0.37.
- **F7:** None of the other angles shows a graded pattern. The 5-day, 20-day and 90-day-high-nearness returns, the short-to-long volatility ratio, volatility terciles and weekdays all have Spearman between −0.033 and +0.014 against the 5-day excess return. Their quintile t-statistics fall between −2.41 and +2.29 with no monotone order.

## Ideas
- No ideas: I looked at about 35 groupings: six bar variables in quintiles, volatility terciles, weekday, year, coin, side and the book's tails. The only cell beyond t 2.5 is the large-up-day continuation (F6, t 2.66), and it is neither graded nor consistent across coins. That does not stand out from chance given how many angles were tried, so no finding supports a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
