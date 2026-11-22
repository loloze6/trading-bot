# Backtest of 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1044 | 0.024675 | -32.307 |
| w2 | 1054 | -0.003833 | -44.163 |
| w3 | 971 | 0.025156 | -15.646 |
| w4 | 941 | 0.01351 | -2.322 |
| w5 | 1015 | 0.032175 | -52.875 |
| w6 | 958 | 0.026724 | 6.154 |
| w7 | 1074 | 0.015989 | -19.362 |
| w8 | 1017 | -0.002341 | -14.014 |
| w9 | 1039 | 0.010873 | -41.077 |
| w10 | 980 | 0.040124 | 16.909 |
| w11 | 1066 | 0.039974 | 38.587 |
| w12 | 1112 | -0.012471 | -21.984 |
| w13 | 1046 | 0.036239 | 15.434 |
| w14 | 1029 | 0.003927 | -54.783 |
| w15 | 1033 | 0.028318 | 45.85 |
| w16 | 988 | 0.038682 | -24.455 |
| w17 | 957 | -0.003098 | 31.357 |
| w18 | 1038 | -0.003592 | -32.31 |
| w19 | 965 | 0.019949 | 2.3 |
| w20 | 1001 | 0.008171 | -22.712 |
| w21 | 1041 | 0.066605 | 50.991 |
| w22 | 943 | 0.022784 | -10.105 |
| w23 | 1057 | 0.036608 | -14.862 |
| w24 | 975 | -0.020516 | -54.374 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1101 | -0.002409 | -46.949 |
| w2 | 1106 | -0.01565 | -39.855 |
| w3 | 1038 | -0.011692 | -26.307 |
| w4 | 985 | 0.009192 | -19.748 |
| w5 | 1057 | 0.01143 | -55.105 |
| w6 | 1032 | -0.006751 | -28.577 |
| w7 | 1259 | 0.048786 | -26.807 |
| w8 | 1010 | 0.021422 | -4.768 |
| w9 | 1157 | 0.017848 | -32.533 |
| w10 | 1073 | 0.035644 | 23.951 |
| w11 | 1087 | 0.018413 | 42.996 |
| w12 | 1147 | 0.014297 | -0.986 |
| w13 | 511 | 0.020532 | 7.883 |
| w14 | 1065 | -0.009336 | -30.486 |
| w15 | 1073 | 0.028207 | 51.356 |
| w16 | 1029 | 0.052553 | 24.411 |
| w17 | 1067 | -0.019809 | 3.753 |
| w18 | 1106 | -0.014087 | -17.588 |
| w19 | 971 | -0.00879 | 5.92 |
| w20 | 1061 | 0.0191 | -37.756 |
| w21 | 1036 | 0.058977 | 29.647 |
| w22 | 1039 | -0.019819 | -45.276 |
| w23 | 1043 | 0.01391 | 26.924 |
| w24 | 1019 | -0.044923 | -43.754 |

