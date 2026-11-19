---
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation_1h
idea tested: 016-02_down-grind-price-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3416 USD
---
## Findings
- **F1:** The book loses through fees and short drag, not through the forecast itself: it averaged -0.000756 a day (t -7.32, n 17381) while holding the coins averaged +0.00119; per day its gross gain was -0.000068, its fees 0.000728, being short in a rising market cost about -0.00034 (-0.000014 per bar), and timing earned only about +0.00026 (+0.000011 per bar).
- **F2:** The fees come almost entirely from switching on and off: 0.67 entries and 0.67 exits a day carry 99.4 % of the fee, while resizes carry 0.6 %, because the position follows the flipping sign of the 3-day return.
- **F3:** The grind grading is close to empty: once active, the forecast sits at mean -9.99 with standard deviation 0.74, so the book is in effect a fixed short; the four forecast quartiles' excess 72-bar returns (0.0008, -0.0039, 0.0001, -0.0030) do not rise with grind, and the main measure's t is 0.95 over 2762 grid bars.
- **F4:** Falls continue only when they are quiet: among active grid bars, those whose 3-day hourly volatility over 30-day hourly volatility was lowest (ratio 0.57 and 0.79) were followed by excess 72-bar returns of -0.0070 (t -1.98, n 509) and -0.0074 (t -2.24, n 509), and those with the highest ratio (1.01 and 1.48) by +0.0024 and +0.0048; the graded Spearman of the ratio against excess return is 0.07 (t 2.14, n 2035).
- **F5:** Inside quiet falls both grind halves continued (-0.0088 for the lower half of the grind measure and -0.0053 for the upper half, n about 520 each), while in turbulent falls both were flat or reversed (+0.0001 and +0.0068), so the volatility state carries the effect and grind share adds little to it.
- **F6:** Small falls continued and large falls reversed: the smallest 3-day falls (mean -0.8 %) were followed by -0.0098 excess, and the largest (mean -13.2 %) by +0.0041 (n about 667 each); falls inside a strong 30-day rise (mean +34 %) were followed by +0.0040 (t 1.02, n 509).
- **F7:** Being short in turbulent hours lost money on a bar level: on short bars in the top volatility-ratio quarter the daily-scaled gross was -0.0017, against +0.0007 in the calmest quarter.

## Ideas
- `016-02_down-grind-price-continuation.d1_quiet-grind-falls-continue` (from F1, F3, F4, F5, F7): When a coin has fallen over the past 3 days, the larger the share of that fall made by many small hourly losses in the same direction, rather than by its few biggest hours, the more the coin keeps falling over the next 3 days, and the more so the lower its hourly volatility over those 3 days stands against its hourly volatility over the past 30 days.
- `016-02_down-grind-price-continuation.d2_quiet-falls-keep-falling` (from F4, F5, F6, F7): The lower a coin's hourly volatility over the past 3 days stands against its hourly volatility over the past 30 days while it has fallen over those 3 days, the more the coin keeps falling over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
