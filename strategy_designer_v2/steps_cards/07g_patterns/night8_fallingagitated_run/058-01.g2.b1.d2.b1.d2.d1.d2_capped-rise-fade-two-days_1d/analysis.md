---
line: 7.g patterns
backtest: 058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days_1d
idea tested: 058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4198 USD
---
## Findings
- **F1:** In the falling, agitated profile (folds B, C), a one-day rise of up to one 30-day standard deviation is followed by a next-day return 1.02 % below the coin's normal drift (517 cases, day-clustered t −2.23 over 207 days). That is about 4.6 times the 0.22 % cost of a trade. Over 2 days the same rises give back only 0.29 % to 0.46 % (bins 0–0.5 and 0.5–1, t −0.26 and −0.29), so the give-back sits in the first day and the tested 2-day hold dilutes it.
- **F2:** The next-day give-back after a rise of up to one swing points the same way in every year shown: 2018 −2.16 % (t −2.48), 2019 −0.89 % (t −2.07), 2020 −0.16 % (t −0.21), 2021 −1.18 % (t −1.22). It also points the same way on all 10 coins, from −0.15 % on XRP to −2.56 % on LINK, with BTC −1.09 % (t −2.18), LTC −1.52 % (t −2.56) and ZEC −1.30 % (t −2.10).
- **F3:** Inside the profile, the next-day move is graded against the day's scaled return. The Spearman correlation is −0.21 in the profile against −0.08 outside it. Up days of 0–0.5 swing are followed by −0.95 % (t −1.86) and up days of 0.5–1 swing by −1.17 % (t −1.75). Above one swing the effect fades: −0.17 % (t −0.24) for 1–2 swings and +0.21 % for more than 2.
- **F4:** Rises over several days do not show the brief's give-back the next day. Two-day scaled rises of 0–0.5 are followed by −0.40 % (t −0.88), and those of 0.5–1 and above 1 by +0.31 % and +0.55 % (t 0.47 and 0.55). Three-day rises over 2 days are mixed in sign across bins (+1.20 %, −1.87 %, +0.92 %, −5.36 %).
- **F5:** The strongest other pattern in the profile is the rebound after down days, which is not a discovery: the map's falling-agitated long cell already holds 12 strategies for it. Days down more than 2 swings are followed by +6.2 % the next day, days down 1–2 swings by +2.2 % (t 1.81), and wide-range down days by +4.7 % over 2 days (t 2.87, 48 days).
- **F6:** Weekday effects outside the profile do not survive day clustering, so they count as chance. Wednesdays average −0.61 % (t −1.46, 204 days), Thursdays +0.50 % (t 1.49) and Fridays +0.44 % (t 1.60). Close position within the day's range shows no pattern over 2 days (no bin with |t| above 0.8).

## Ideas
- `058-01.g2.b1.d2.b1.d2.d1.d2.g1_capped-rise-fade-next-day` (from F1, F2, F3, F4): In a falling, agitated market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the larger the fall over the next day, while that rise stays within about one usual swing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
