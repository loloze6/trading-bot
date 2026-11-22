# Backtest of 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 123 | 0.040955 | 13.185 |
| w2 | 131 | 0.004889 | -22.122 |
| w3 | 125 | 0.046224 | -8.668 |
| w4 | 160 | 0.019114 | 39.395 |
| w5 | 117 | 0.000668 | 5.241 |
| w6 | 202 | 0.032471 | 28.37 |
| w7 | 170 | 0.024972 | 1.797 |
| w8 | 138 | -0.013505 | 11.822 |
| w9 | 108 | 0.041767 | 6.578 |
| w10 | 156 | -0.002072 | 3.035 |
| w11 | 241 | -0.004452 | 13.435 |
| w12 | 170 | -0.013311 | -21.774 |
| w13 | 194 | 0.013281 | 1.75 |
| w14 | 134 | 0.017911 | -9.724 |
| w15 | 174 | 0.018074 | 50.234 |
| w16 | 228 | -0.010791 | 6.171 |
| w17 | 284 | 0.008879 | 27.721 |
| w18 | 200 | 0.004174 | 10.516 |
| w19 | 180 | 0.026239 | 4.441 |
| w20 | 138 | 0.011885 | 5.447 |
| w21 | 173 | 0.032415 | 24.146 |
| w22 | 115 | 0.005874 | -5.123 |
| w23 | 164 | 0.007179 | -3.605 |
| w24 | 141 | -0.037643 | -10.92 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 133 | 0.013686 | -1.548 |
| w2 | 143 | -0.003573 | 2.237 |
| w3 | 145 | -0.002159 | 4.76 |
| w4 | 172 | 0.020791 | 38.587 |
| w5 | 117 | 0.01442 | -19.2 |
| w6 | 158 | 0.021081 | 17.758 |
| w7 | 158 | 0.037924 | -5.936 |
| w8 | 182 | -0.00932 | 22.131 |
| w9 | 166 | 0.036763 | -7.081 |
| w10 | 193 | 0.032404 | 72.659 |
| w11 | 287 | 0.021329 | 34.521 |
| w12 | 208 | -0.007401 | -17.573 |
| w13 | 131 | 0.010871 | 30.249 |
| w14 | 141 | 0.000257 | 3.734 |
| w15 | 167 | 0.016676 | 9.028 |
| w16 | 218 | -0.010923 | 56.728 |
| w17 | 192 | 0.008271 | 2.719 |
| w18 | 207 | 0.015896 | 30.395 |
| w19 | 209 | 0.007129 | 25.796 |
| w20 | 113 | -0.016063 | 13.413 |
| w21 | 134 | 0.032572 | -3.392 |
| w22 | 148 | -0.014347 | -24.655 |
| w23 | 184 | 0.01505 | 22.365 |
| w24 | 108 | -2.7e-05 | -11.785 |

