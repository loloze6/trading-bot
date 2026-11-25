---
line: 7.g patterns
backtest: 032-02.b1_choppy-downside-break-one-day-rebound_1d
idea tested: 032-02.b1_choppy-downside-break-one-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4138 USD
---
## Findings
- **F1:** Across all profiles, the next-day rebound after a close below the prior 20-day low grows with the break's percent depth. The slope of the next-day unusual move on the close's distance from that low is -0.447 (t -4.90, 294 cases on 106 days), so a deeper break is followed by a larger rise. This is the strongest of the roughly 40 angles examined.
- **F2:** The depth gradient is not confined to the choppy market. In the trending profiles (rising or falling) the slope is -0.414 (t -3.93, 259 cases, 100 days). In the choppy profile it is -0.668 (t -3.29, 35 cases, 23 days).
- **F3:** In the trending profiles, the deepest third of downside breaks is followed by a +2.42 % next-day unusual move (t 1.72, 88 cases, 34 days), the middle third by +0.78 % and the shallowest third by -0.10 %. All downside breaks together give +1.24 % (t 1.80, 294 cases, 106 days), against a trade cost of 0.19 %.
- **F4:** The gradient weakens when depth is measured in units of the coin's 20-day daily volatility (slope t -1.37 over all cases, -1.16 in the trending profiles). So the larger rebounds after deep breaks partly reflect high-volatility episodes. The deep breaks of 2020 averaged +10.0 % on only 4 days, against +1.3 % in 2018 and +1.6 % in 2019.
- **F5:** Upside breaks above the prior 20-day high do not fail the next day. The faded next-day move is -0.25 % over all profiles (t -0.56, 418 cases) and +0.43 % in the choppy profile (t 0.55, 69 cases). The slope on break size is -0.034 (t -0.34). The brief's symmetric claim holds only on the downside.
- **F6:** The other angles show nothing that stands out once the many tests are counted. Large down days (z below -2.5) are followed by +1.40 % (t 1.17). Weekdays all have |t| ≤ 1.54, volatility terciles all have |t| ≤ 0.56, and the windows point mostly the same way, with w14, w15 and w9 slightly negative.

## Ideas
- `032-02.b1.g1_downside-range-break-rebounds` (from F1, F2, F3): In any market, when a coin's daily close falls below the lowest low of its prior 20 days, its price rises over the next day, and the further the close sits below that low in percent, the larger the rise.
- `032-02.b1.g2_agitated-downside-break-rebound` (from F1, F4): In an agitated market, when a coin's daily close falls below the lowest low of its prior 20 days, its price rises over the next day, and the further the close sits below that low in percent, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
