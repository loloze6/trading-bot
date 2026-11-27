---
line: 7.g patterns
backtest: 074-01.b1.b1_falling-wide-up-day-high-close-fade_1d
idea tested: 074-01.b1.b1_falling-wide-up-day-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4922 USD
---
## Findings
- **F1:** In a falling market (60-day return below -10 %), the next-day excess return after an up day grows more negative with the day's range against its 20-day mean range: -0.37 % (<0.8×, n 699), -0.56 % (0.8-1.2×, n 330), -0.72 % (1.2-1.5×, n 118), -0.85 % (1.5-2×, n 94) and -2.31 % (>2×, t -2.39, n 55 on 32 days), all in folds B and C.
- **F2:** The tested idea's second grading, close location, does not hold among falling-market up days with a range of at least 1.5×. Days closing in the top tenth of their range were followed by -0.02 % (t -0.02, n 33). Days closing at 0.66-0.9 were followed by -2.04 % (t -2.26, n 79), and days at 0.33-0.66 by -1.15 % (n 24). The fade does not grow as the close nears the high, so the close-location half of the forecast adds noise to the width half.
- **F3:** Rising markets do not show the fade. Rising-market up days wider than 2× were followed by +2.11 % (t 1.72, n 147, 91 days). Falling markets gave -2.31 % for the same width, so the fade is specific to the falling profile, as the brief claims. This rising-market continuation is already held in the map's rising cells (034-01.e1, 034-02), so it is not a discovery.
- **F4:** The falling-market wide-up-day fade (range ≥ 1.5×) was negative in three of four years: 2018 -1.65 % (n 62), 2019 -1.65 % (n 21), 2020 -2.58 % (n 29). It was about zero in 2021 (+0.14 %, n 37), so the effect is uneven over time.
- **F5:** The book's gain rests on a handful of days. Over 1,449 days its daily returns sum to +0.063, against +0.204 for its 10 best days and -0.181 for its 10 worst. This fits a forecast diluted by a close-location measure that, per F2, does not sort the cases.
- **F6:** Choppy-market days closing in their bottom tenth were followed by -1.89 % (t -2.85, n 46). This is not graded: closes at 0.1-0.33 were followed by +0.96 % (t 2.10), and the Spearman correlation between how low a choppy day closes and its next-day excess is +0.06 (n 959). Among the roughly 100 cells examined it does not stand out as a pattern.

## Ideas
- `074-01.b1.b1.g1_falling-wide-up-day-width-fade` (from F1, F2, F3, F4): In a falling market, an up day whose high-to-low range is wide compared with the coin's average daily range over the past 20 days is followed by a fall over the next day, and the wider that range against the 20-day average, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
