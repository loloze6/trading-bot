---
line: 7.a not observable
backtest: 003-02_thin-volume-drop-rebounds_1d
idea tested: 003-02_thin-volume-drop-rebounds
step 5: not observable
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2015 USD
---
## Findings
- **F1:** The situation the idea needs almost never occurs. Of 13,348 daily bars on 6 coins over 24 windows, 381 bars (2.9%) were falls of at least 2 usual moves and 2,809 (21.0%) had volume at or below half the 30-day average, but only 4 bars were both. The step-5 count of 5 independent events is well short of the plan's minimum of 20.
- **F2:** Sharp falls come on heavy volume, not thin. Among the 381 sharp falls, only 1.05% had a volume ratio of 0.5 or less, and the median ratio was 1.72. The 5% quantile was 0.73 and the 10% quantile was 0.96. So a sharp fall at half the average volume lies in the extreme tail of the fall distribution.
- **F3:** The rare cases are spread thinly and do not depend on the year or the bar size of the test window. They fell only in XMR (2) and ZEC (2), and none in BTC, ETH, LTC or XRP. By year, 2019 had 1, 2021 had 2, 2022 had 1, and the other five years had 0. That is about 0.08 cases per coin-year, and 0.25 per coin-year even in the two thinnest coins.
- **F4:** The outcome varies widely from case to case. The excess 5-day return after any sharp fall had a standard deviation of 0.104 across 371 cases, against a mean of -0.004 (t = -0.74). With that spread, a few cases cannot settle the 0.113 mean seen in the 4 thin-volume falls, whose standard deviation was 0.088.

## Ideas
- No ideas: The plan needs at least 20 independent thin-volume sharp falls. The default data gave 4 over about 48 coin-years. All the available daily data comes to roughly 100 coin-years: the 6 default coins over 8 years, about 33 coin-years of ADA/DOGE/LINK/TRX/UNI/AAVE, about 12 of AVAX/SOL/INJ and about 8 of the fold-D coins. At the observed rate that would give about 8 cases, and even at the thin-coin rate of XMR and ZEC only about 17. Since only daily bars are available, no data available would reach the minimum of 20.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
