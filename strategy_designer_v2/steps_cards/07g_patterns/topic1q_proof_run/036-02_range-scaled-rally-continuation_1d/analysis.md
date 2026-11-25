---
line: 7.g patterns
backtest: 036-02_range-scaled-rally-continuation_1d
idea tested: 036-02_range-scaled-rally-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6050 USD
---
## Findings
- **F1:** In a falling, agitated market (60-day return below -10 %; 30-day swing above its running median, a within-window stand-in for the profile's one-year median), a larger up-day measured against the 30-day mean daily range is followed by a larger 3-day loss against the coin's drift: slope t -3.89 on 135 non-overlapping up-day cases. By s1 quartile the 3-day excess return is +0.94 %, -0.75 %, -3.40 % and -6.15 % (t -2.51 on 14 days); the vol-scaled quartiles give the same order (+1.41 % down to -5.13 %, t -2.38).
- **F2:** That falling-agitated fade holds outside any one year or coin. The top quartile is negative in every year (2018 -7.18 %, 2019 -2.96 %, 2020 -6.98 %, 2021 -4.08 % on one case) and in 5 of 6 coins with t_day ≤ -2.27 (BTC -11.5 %, ETH -6.5 %, LTC -8.5 %, XMR -5.1 %, XRP -9.7 %; ZEC -0.07 %). In falling calm markets the slope is weak (t -0.80, n 215).
- **F3:** The fade peaks at 3 days. The slope t is -1.82 at 1 day, -2.82 at 2 days, -3.89 at 3 days and -1.74 at 5 days. Over 7 days the falling-market top-s1 quintile is only -1.40 % (t -0.47), which is why the tested 7-day horizon misses it.
- **F4:** The mirror holds in rising, agitated markets: a larger range-scaled up-day is followed by a larger 3-day gain (slope +0.047, t 5.13, 135 cases). In rising calm markets there is none (t 0.46), and in choppy markets none either (t -1.10 and -0.61).
- **F5:** The tested idea itself shows no grading. The 7-day excess return by s3 decile runs from +0.85 % to +1.09 % with no order (top decile t 0.53). The big-up-3 cases in falling markets average -2.96 % (t -1.33), against +1.28 % for small ones. The step-5 size is -0.15 % (t -0.33, 875 days).
- **F6:** On all bars, the next day partly reverses the range-scaled 1-day move: the bottom decile is +0.85 % (t 3.77) and the top decile -0.49 % (t -2.17). On the down side this repeats the falling-agitated rebound books the map already holds, so no idea is written from it.
- **F7:** Next-day excess after Wednesdays is -0.66 % (t -3.33), but it comes from 2019 alone (-1.57 %, t -3.24; the other years run from -0.44 % to +0.23 %, all |t| < 0.5). After the many angles looked at, this is not a finding to build on.

## Ideas
- `036-02.g1_falling-agitated-rally-fades` (from F1, F2, F3, F5): In a falling, agitated market, a coin whose 1-day return is large against its average daily high-to-low range over the past 30 days falls over the next 3 days, and the larger that range-scaled one-day rise, the larger the fall.
- `036-02.g2_rising-agitated-rally-continues` (from F4, F3): In a rising, agitated market, a coin whose 1-day return is large against its average daily high-to-low range over the past 30 days keeps rising over the next 3 days, and the larger that range-scaled one-day rise, the larger the further gain.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
