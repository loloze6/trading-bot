# Backtest of 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 121 | 0.002222 | -25.98 |
| w2 | 123 | -0.010446 | -50.638 |
| w3 | 137 | -0.011167 | -19.171 |
| w4 | 130 | 0.039035 | 141.952 |
| w5 | 149 | 0.01487 | -26.718 |
| w6 | 133 | -0.021821 | 126.742 |
| w7 | 133 | -0.013487 | -12.24 |
| w8 | 146 | 0.024583 | 38.29 |
| w9 | 154 | 0.044606 | -33.032 |
| w10 | 150 | -0.03125 | 22.716 |
| w11 | 96 | -0.003601 | 59.082 |
| w12 | 127 | 0.014324 | 2.067 |
| w13 | 113 | 0.00209 | -12.585 |
| w14 | 147 | -0.033552 | -65.908 |
| w15 | 119 | 0.013242 | 89.873 |
| w16 | 107 | 0.012921 | -35.098 |
| w17 | 122 | -4e-05 | 243.067 |
| w18 | 106 | 0.024377 | -26.897 |
| w19 | 131 | -0.010474 | 69.862 |
| w20 | 144 | -0.025745 | -15.158 |
| w21 | 108 | 0.015017 | 126.726 |
| w22 | 113 | -0.009548 | -10.441 |
| w23 | 123 | -0.031297 | -1.364 |
| w24 | 143 | 0.003391 | -48.414 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 99 | -0.026311 | -28.129 |
| w2 | 111 | 0.016216 | -37.85 |
| w3 | 125 | 0.023337 | -18.202 |
| w4 | 146 | 0.017343 | 72.772 |
| w5 | 164 | -0.011654 | -43.909 |
| w6 | 140 | -0.009884 | 38.982 |
| w7 | 119 | -0.010005 | -41.388 |
| w8 | 140 | -0.003243 | 17.366 |
| w9 | 153 | 0.004758 | -29.099 |
| w10 | 129 | -0.002135 | 176.834 |
| w11 | 97 | 0.014498 | 144.465 |
| w12 | 123 | 0.009363 | 16.415 |
| w13 | 83 | 0.007029 | 33.507 |
| w14 | 127 | -0.004536 | -47.493 |
| w15 | 104 | -0.024884 | 16.745 |
| w16 | 110 | -0.00464 | 56.902 |
| w17 | 104 | 0.008377 | 50.005 |
| w18 | 99 | 0.054834 | 35.521 |
| w19 | 127 | -0.010583 | 50.676 |
| w20 | 125 | -0.009329 | -22.178 |
| w21 | 125 | -0.024843 | 39.062 |
| w22 | 124 | 0.036392 | -43.816 |
| w23 | 107 | 0.017522 | 105.842 |
| w24 | 126 | 0.007838 | -53.189 |

