---
line: 7.g patterns
backtest: 060-01.g1.g1_graded-width-high-close-fade_1d
idea tested: 060-01.g1.g1_graded-width-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4244 USD
---
## Findings
- **F1:** Inside the falling agitated profile, days that did not fall (one-day return above −0.77 %) are followed by a next-day excess fall in every year shown: −1.49 % in 2018 (t −1.92), −1.15 % in 2019 (t −2.62), −0.30 % in 2020 (t −0.45) and −0.75 % in 2021 (t −0.81). The fall also shows on 5 of 6 coins: BTC −1.09 % (t −2.86), XMR −1.06 % (t −2.09), ZEC −1.00 % (t −2.11), LTC −0.99 % (t −1.99), ETH −0.82 % (t −1.86). XRP is weak at −0.34 % (t −0.37).
- **F2:** Inside the profile, the flat-day and small-up-day return quintiles fade harder than the close-location bins do. Flat days (−0.77 % to +0.93 %) fall −1.05 % next day (strength −0.21, t −2.43, 221 cases, 149 days) and small up days −1.13 % (t −1.86, 206 cases). By close location, closes at 0.6–0.8 of the range fall −0.84 % (t −1.80) and closes at 0.8–1.0 fall −0.49 % (t −0.76).
- **F3:** Inside the profile, among upper-half closes, the next-day fall grows with the day's width against its last 20 days. By width quartile it is −0.10 %, −0.55 %, −1.09 % and −1.55 % (top quartile t −1.78, 91 cases, 55 days). Outside the profile the same quartiles show no steady pattern (−0.13 %, −0.47 %, −0.40 %, −0.00 %).
- **F4:** Over all bars, the next-day fall after an up day grows with the coin's own 20-day swing. By swing tercile it is +0.20 % (t 1.01), −0.34 % (t −1.80) and −0.79 % (t −2.58, 1,296 cases). In the top tercile, up days fall −0.90 % in a falling 60-day trend (t −1.65) but rise +0.25 % in a rising one. So the fade belongs to the falling, agitated market the brief names.
- **F5:** Inside the profile, down days rebound strongly: bottom return quintile +2.18 % next day (strength 0.41, t 3.78, 358 cases, 152 days). This is not used here: the brief is short only, and the falling-agitated long cell already holds 12 strategies.
- **F6:** The book gains mainly when the coins fall: the book's daily returns move against the coins' (correlation −0.34) and are in a position on 12 % of days. Only w14 (+0.10 % a day) stands clearly above zero. Weekday, 5-day return and candle-body groupings showed nothing that stands out across the many angles looked at (best t −2.08 for one body quintile, with no gradient).

## Ideas
- `060-01.g1.g1.g1_agitated-downtrend-up-day-fade` (from F1, F2, F3): In a falling, agitated market, a day on which the coin closes above the previous day's close is followed by a fall over the next day, and the wider that day's high-low range against its ranges of the last 20 days, the larger the fall.
- `060-01.g1.g1.g2_swing-graded-downtrend-rally-fade` (from F1, F4): In a falling, agitated market, a day on which the coin closes above the previous day's close is followed by a fall over the next day, and the larger the coin's swing over the last 20 days against its swings of the past year, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
