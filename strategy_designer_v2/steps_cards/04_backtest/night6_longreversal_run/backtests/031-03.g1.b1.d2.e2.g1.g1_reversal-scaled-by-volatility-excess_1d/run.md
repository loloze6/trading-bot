# Backtest of 031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1_reversal-scaled-by-volatility-excess_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XMR as XMRUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 104 | 0.037199 | -7.519 |
| w2 | 113 | 0.107526 | 17.086 |
| w3 | 112 | 0.140317 | 5.797 |
| w4 | 112 | 0.116582 | 6.449 |
| w5 | 114 | -0.017917 | -30.074 |
| w6 | 117 | 0.09321 | -12.392 |
| w7 | 107 | 0.153413 | 23.714 |
| w8 | 109 | 0.180966 | 14.613 |
| w9 | 107 | 0.055681 | -3.668 |
| w10 | 104 | 0.34106 | 63.336 |
| w11 | 108 | 0.076258 | 0.651 |
| w12 | 105 | 0.004575 | -8.97 |
| w13 | 107 | 0.151763 | 41.748 |
| w14 | 110 | 0.146907 | 30.083 |
| w15 | 109 | -0.026811 | -22.921 |
| w16 | 111 | 0.149171 | 18.879 |
| w17 | 115 | 0.204049 | 46.384 |
| w18 | 104 | 0.21395 | 53.824 |
| w19 | 112 | 0.139621 | 33.247 |
| w20 | 102 | 0.179274 | 14.789 |
| w21 | 106 | 0.062554 | -15.812 |
| w22 | 106 | 0.072476 | -3.279 |
| w23 | 109 | -0.109505 | -44.874 |
| w24 | 103 | -0.009086 | -18.912 |

