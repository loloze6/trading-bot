---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size
line: 7.g patterns
backtest: 024-02_fading-volume-downrun-rebound-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day rise relative to its typical 4-hour move over the past 30 days, and the higher its volume over those 3 days relative to its 30-day volume, the more the coin keeps rising over the next 3 days.
Consequence: A trader would buy a strong rise that comes with heavy volume, rather than fade it, and would hold back from a strong rise made on light volume.
Why:
- F2: Large rises tend to continue rather than give back. The top quintile of the 3-day return in usual 4h moves (mean +9.3 usual moves) has a next-3-day strength of +0.104 (t 3.03, 1032 cases). The bottom quintile, the large falls the tested idea bets on, shows only +0.023 (t 0.72). The top quintile of the 7-day return has +0.098 (t 2.77, 1032 cases).
- F3: That continuation depends on high volume. Take the top tercile of the 3-day return and split it by 3-day volume against the 30-day volume. With the highest volume its strength is +0.134 (t 3.12, 738 cases); with the lowest volume it is −0.029 (t −0.65, 433 cases). This contradicts the brief's claim that fading-volume runs give back more.
- F4: The continuation is not steady across coins, years or the full range of returns. In the top 3-day-return tercile, strength is positive in 5 of 6 coins but no coin reaches t 2 (t −0.20 to 1.70). It is negative in 2018, 2019, 2022 and 2025 (−0.062, −0.050, −0.093, −0.016) and positive in 2020, 2021, 2023 and 2024 (+0.221, +0.165, +0.061, +0.129). The per-coin rank correlation between the 3-day return and the following strength lies between −0.045 and +0.031.
