---
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days_1d
idea tested: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3806 USD
---
## Findings
- **F1:** The book's gain comes from its long days, while its short days lose to the coins' rise. The book's mean daily return is +0.149 % on long days (8,657 coin-days) and −0.018 % on short days (8,671). The market's own rise accounts for +0.071 % of the long days' return and −0.058 % of the short days' return. So timing adds about +0.08 % a day long and +0.04 % a day short, but the shorts' timing does not cover the drift they pay.
- **F2:** Long trades earn through a few very large winners, and short trades lose steadily. There are 2,590 long trades, with a mean of +7.7 % net, a median of −0.8 % and a standard deviation of 62 %; for ZEC alone the mean is +24 % and the median −2.2 %. There are 2,974 short trades, with a mean of −2.4 % and a median of −2.6 %, negative on all 6 coins (medians −1.9 % to −3.7 %). The best 1 % of book days are 71 % long; the worst 1 % are 55 % long.
- **F3:** The 28-day momentum effect is the same size on both sides. In units of the coin's usual 10-day move, its signed excess 10-day return is +0.043 after rises (t 1.06, 644 cases) and +0.032 after falls (t 0.88, 615 cases). The long/short gap in F1 and F2 is drift and skew, not a stronger signal on one side.
- **F4:** The effect changes sign from year to year, and the negative years match the book's weak Calmar of 0.31. The signed excess is about +0.10 to +0.16 in 2020, 2021, 2024 and 2025 (t up to 1.98). It is −0.10 in 2022 and −0.07 in 2023 (t −1.51 and −1.35), and the book's mean daily return was −0.10 % in 2023. No single year is significant on about 156 cases each.
- **F5:** Large days are not followed by short reversals on these daily bars. The Spearman correlation between the 1-day return scaled by 20-day volatility and the excess 3-day return is −0.036. No bin is significant (t between −1.29 and 0.93; 147 cases after days below −2 volatility units, 169 after days above +2).
- **F6:** Nearness to the 60-day high leans in momentum's direction but does not stand out from chance. The excess 10-day return by quintile runs −0.048, −0.047, −0.050, +0.070 and +0.106 of the usual move (top quintile t 1.72, 252 cases). The Spearman correlation is 0.046, and 5 of 6 coins show top-minus-bottom differences of +0.05 to +0.28; XMR shows −0.09.
- **F7:** No pattern stands out by volatility level. Of about 30 groupings looked at, the only one at t 2 is momentum's strength in the middle volatility tercile (+0.089, t 2.04, 419 cases). The low tercile gives −0.024 (t −0.58) and the high one +0.047 (t 0.86), and the book's mean daily return barely changes across terciles (0.080 %, 0.071 %, 0.061 %).

## Ideas
- No ideas: Across about 30 angles (forecast, the 1-, 5-, 28- and 60-day returns, volatility, nearness to highs, reversal after large days, year, coin, side, trades), no pattern beyond the tested momentum stands out from chance: nothing passes t 2 except one volatility tercile at 2.04. The long/short gap in F1 to F3 comes from the coins' drift and the skew of long trades, not from a market effect the idea leaves unexplained.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
