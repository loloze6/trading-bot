# Backtest of 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 112 | 0.007849 | -19.579 |
| w2 | 105 | -0.008544 | -56.726 |
| w3 | 125 | 0.002825 | -19.277 |
| w4 | 130 | 0.018585 | 111.789 |
| w5 | 131 | 0.024383 | -11.914 |
| w6 | 127 | 0.014327 | 101.102 |
| w7 | 123 | 0.01967 | -21.923 |
| w8 | 142 | -0.044893 | 62.16 |
| w9 | 120 | -0.000495 | -27.197 |
| w10 | 142 | 0.040232 | 26.203 |
| w11 | 121 | 0.051938 | 70.668 |
| w12 | 144 | -0.027409 | -27.585 |
| w13 | 118 | 0.037826 | -17.907 |
| w14 | 132 | -0.008523 | -62.169 |
| w15 | 121 | 0.011247 | 107.198 |
| w16 | 138 | 0.045767 | -40.878 |
| w17 | 131 | 0.007421 | 145.04 |
| w18 | 127 | 0.00862 | -3.628 |
| w19 | 126 | 0.022485 | 41.891 |
| w20 | 125 | -0.006734 | -14.744 |
| w21 | 117 | 0.051289 | 132.222 |
| w22 | 125 | 0.023958 | 0.335 |
| w23 | 113 | 0.043334 | 10.693 |
| w24 | 117 | -0.012605 | -52.487 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 96 | -0.009458 | -27.325 |
| w2 | 123 | -0.015174 | -48.583 |
| w3 | 130 | -0.027557 | -18.105 |
| w4 | 130 | 0.021986 | 69.372 |
| w5 | 131 | -0.016758 | -28.858 |
| w6 | 107 | 0.010796 | 34.62 |
| w7 | 111 | 0.060784 | -42.41 |
| w8 | 152 | 0.013042 | 25.764 |
| w9 | 141 | 0.00346 | -34.735 |
| w10 | 155 | 0.030456 | 130.312 |
| w11 | 114 | 0.038062 | 144.795 |
| w12 | 131 | 0.018001 | 4.491 |
| w13 | 80 | 0.037024 | -1.421 |
| w14 | 118 | -0.026158 | -51.655 |
| w15 | 117 | 0.012246 | 29.874 |
| w16 | 106 | 0.02047 | 8.438 |
| w17 | 138 | -0.007646 | 30.442 |
| w18 | 129 | -0.01239 | 11.97 |
| w19 | 119 | 0.013355 | 66.542 |
| w20 | 120 | 0.015221 | -26.17 |
| w21 | 106 | 0.05272 | 58.083 |
| w22 | 125 | -0.008823 | -50.279 |
| w23 | 113 | 0.016394 | 139.325 |
| w24 | 125 | -0.027261 | -45.97 |

