# Backtest of 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XMR as XMRUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | -0.009149 | -11.063 |
| w2 | 47 | 0.089518 | 3.857 |
| w3 | 37 | 0.137112 | 4.486 |
| w4 | 47 | 0.154908 | 17.657 |
| w5 | 50 | 0.051878 | -12.121 |
| w6 | 51 | 0.174362 | 16.749 |
| w7 | 57 | 0.196571 | 13.359 |
| w8 | 47 | 0.202261 | 23.695 |
| w9 | 58 | 0.046762 | -10.291 |
| w10 | 40 | 0.307542 | 41.806 |
| w11 | 40 | 0.023959 | 21.487 |
| w12 | 42 | 0.02451 | -5.263 |
| w13 | 51 | 0.142923 | 23.019 |
| w14 | 55 | 0.148018 | 2.808 |
| w15 | 49 | -0.034966 | -8.379 |
| w16 | 55 | 0.120237 | 14.425 |
| w17 | 45 | 0.164023 | 36.133 |
| w18 | 46 | 0.260478 | 44.497 |
| w19 | 52 | 0.216445 | 22.735 |
| w20 | 36 | 0.252907 | 27.145 |
| w21 | 44 | 0.046613 | 2.745 |
| w22 | 40 | 0.108027 | 17.334 |
| w23 | 55 | -0.095333 | -22.143 |
| w24 | 43 | -0.084968 | -4.958 |

