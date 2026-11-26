---
line: 7.g patterns
backtest: 058-02.b1.g1.b1_falling-rally-fades-more-coins_1d
idea tested: 058-02.b1.g1.b1_falling-rally-fades-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6606 USD
---
## Findings
- **F1:** The brief's claimed reversion is not in these bars; the 20-day range position continues instead. In choppy calm markets, over the next 3 days on a non-overlapping grid, closes at 0.7–0.9 of the 20-day close range gained +2.86 % over the coin's drift (t 2.06, 42 cases), while closes at 0.1–0.3 lost −3.77 % (t −2.50, 42 cases), against −0.46 % for the middle (t −0.45, 87 cases). This meets two of the brief's own falsification conditions (tops rise more than the middle, bottoms do not rise).
- **F2:** The continuation in choppy calm markets is graded, but its t sits near 2. The signed range position (−1 at the bottom, +1 at the top) times the next-3-day excess return averages +1.56 % (t 1.80, 258 cases, 102 days) on the 20-day range and +1.72 % (t 1.93) on the 30-day range, with a positive slope (+2.06 % per unit). It is positive in every year shown: 2018 +1.37 %, 2019 +0.14 %, 2020 +1.70 %, 2021 +2.24 %.
- **F3:** The same continuation shows in every calm profile and is weaker in the agitated ones. Next-3-day signed continuation is +1.42 % (t 2.51, 396 cases) falling calm, +0.93 % (t 1.80) choppy calm and +1.18 % (t 1.85) rising calm, against +0.50 % (t 0.70), +1.67 % (t 1.34) and +0.40 % (t 0.42) in the agitated profiles. This is the calm-market nearness-to-high effect the map already holds (035-01.b1).
- **F4:** The tested fade of up days in falling markets is graded in direction but cannot be told from chance. The falling-market next-day excess runs from +0.60 % (z ≤ −2) to −1.10 % (z > 2), but each bucket has |t| ≤ 1.29. Shorting agitated falling up days earns +0.67 % (t 1.62, 732 cases, 208 days), against step 5's +0.27 % unusual move (t 1.62), which is 1.2 times the 0.22 % cost of a trade.
- **F5:** The strongest pattern in the bars is the rebound after a sharp down day in an agitated market, which the map already holds in 12 falling agitated and 5 choppy agitated long books. Next-day excess is +3.88 % after z ≤ −2 in agitated markets (t 2.93, 119 cases, 52 days), and +8.43 % (t 3.08, 45 cases) in the top volatility tercile, against +0.85 % (t 0.74) in calm markets.
- **F6:** Weekday of the close, the year of up-day fades and the close position within the bar show nothing that stands out. Weekday next-day excess has |t| ≤ 1.48 on every weekday, only 2018 reaches t 2.03 for the up-day short, and the falling agitated up days closing mid-bar give −1.12 % (t −1.93).

## Ideas
- `058-02.b1.g1.b1.g1_choppy-calm-range-continuation` (from F1, F2, F3): In a choppy, calm market, the nearer a coin's close sits to the top of its 20-day range, the larger its rise over the next 3 days. The nearer it sits to the bottom, the larger its fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
