---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day
line: 7.g patterns
backtest: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin rises over the 4 hours from 16:00 to 20:00 UTC, the lower its return over the following 4 hours, from 20:00 to 24:00 UTC.
Consequence: A trader would avoid holding, or would lighten, a coin through the late UTC evening after a strong afternoon rise, more so the stronger the rise.
Why:
- F1: Over the 4 hours from 20:00 UTC, coins earn less than their usual 4-hour drift (−0.071 %, t −4.62, 17373 bars), and the drop is graded by the coin's own move over the preceding 16:00–20:00 UTC bar. By that move's quintile, from lowest to highest, the next 4 hours return +0.007 % (t 0.18), +0.042 %, −0.041 %, −0.135 % (t −4.03) and −0.189 % (t −4.66), about 3190 bars each. It holds in 5 of 6 coins (BTC t −2.58, XRP t −3.66, ZEC t −2.47) but fades after 2022: 2018 −0.302 % (t −5.44), 2022 −0.171 % (t −4.21), 2024 +0.072 %.
- F2: The 16:00–20:00 UTC bar itself returns more than the usual drift (+0.077 %, t 5.15, 17506 bars). It is positive in every year from 2018 to 2025 and in every coin (ETH t 2.86, ZEC t 2.82). So the afternoon rise is partly given back over the next 4 hours.
