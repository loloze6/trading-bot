---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.b1_range-top-continues-in-risers_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, the larger its 20-day return measured in units of its daily volatility, the more it falls over the next 5 days, and the deeper it has fallen the more it rises back.
Consequence: A trader would refuse to chase a sharp 20-day bounce in a coin still down over 90 days, and would lean against it.
Why:
- F3: In the unknown regime (90-day return at or below 0), strength reverses after 2021. Over 2022–2025 the slope of the demeaned 5-day return on the 20-day return in units of 20-day daily volatility is −0.0158 (t −4.55, 721 cases), and on the 30-day range position it is −0.030 (t −2.96, 654 cases). Over 2018–2021 the same slopes are +0.0072 (t 1.65) and +0.030 (t 2.15), so the pooled slope is only −0.0037 (t −1.33).
