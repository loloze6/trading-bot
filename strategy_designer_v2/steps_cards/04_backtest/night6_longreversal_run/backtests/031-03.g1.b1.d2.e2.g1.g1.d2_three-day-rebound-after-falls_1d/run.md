# Backtest of 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XMR as XMRUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 63 | -0.015947 | -15.578 |
| w2 | 65 | 0.090077 | -14.14 |
| w3 | 53 | 0.140022 | 8.098 |
| w4 | 56 | 0.154585 | 36.544 |
| w5 | 55 | 0.044008 | -24.949 |
| w6 | 55 | 0.174719 | 46.777 |
| w7 | 75 | 0.19952 | -2.621 |
| w8 | 66 | 0.201544 | 12.666 |
| w9 | 68 | 0.05555 | -13.238 |
| w10 | 54 | 0.30812 | 54.933 |
| w11 | 53 | 0.02796 | 50.079 |
| w12 | 54 | 0.02465 | 18.027 |
| w13 | 60 | 0.139791 | -2.989 |
| w14 | 65 | 0.147497 | -39.029 |
| w15 | 59 | -0.042326 | 10.607 |
| w16 | 69 | 0.120294 | 4.958 |
| w17 | 53 | 0.16223 | 51.499 |
| w18 | 58 | 0.26136 | -17.918 |
| w19 | 61 | 0.21883 | -13.674 |
| w20 | 52 | 0.236989 | 32.51 |
| w21 | 62 | 0.046775 | -0.344 |
| w22 | 50 | 0.110817 | 17.442 |
| w23 | 65 | -0.092123 | -17.647 |
| w24 | 51 | -0.08876 | 26.823 |

