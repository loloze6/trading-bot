---
line: 7.g patterns
backtest: 038-02_agitated-fall-vs-swing-rebound_1d
idea tested: 038-02_agitated-fall-vs-swing-rebound
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4277 USD
---
## Findings
- **F1:** The scaled-fall rebound grows with the agitation of the coin's current swing, whatever the trend. On days with a fall of more than one 30-day standard deviation, the next day's excess return is +1.77 % (t 4.69, 232 cases) when the coin's 30-day swing ranks in the upper third of its recent swings. It is +0.60 % (t 1.52, 236 cases) in the middle third and -0.22 % (t -0.59, 167 cases) in the lower third, across all trends.
- **F2:** The graded rebound is strongest in the falling agitated profile, is also present in choppy markets, and is absent in falling calm ones. The slope of the next-day excess return on the scaled fall size is:
- **F3:** In the falling agitated profile, the bounce does not fade after the first day. After falls beyond one standard deviation (129 cases), the mean return is +2.91 % over the next day (t 4.46), +2.51 % over two days (t 3.26) and +3.57 % over three days (t 3.84). These are overlapping returns from distinct signal bars, not a non-overlapping grid.
- **F4:** In the falling agitated profile, the next-day excess return rises step by step with the fall's size in standard deviations:
- **F5:** The book's gain is concentrated in a few windows:

## Ideas
- `038-02.g1_agitated-outsized-fall-rebounds` (from F1, F2, F4): In an agitated market, the larger a coin's one-day fall against the standard deviation of its daily returns over the last 30 days, the larger its rise over the next day.
- `038-02.g2_agitated-fall-three-day-rebound` (from F3, F4): In a falling, agitated market, the larger a coin's one-day fall against the standard deviation of its daily returns over the last 30 days, the larger its rise over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
