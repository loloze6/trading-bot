# Backtest of 064-01_falling-calm-up-day-fades_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/064-01_falling-calm-up-day-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 22 | -0.046369 | -1.968 |
| w13 | 8 | -0.074055 | -15.345 |
| w14 | 7 | 0.066131 | -16.666 |
| w15 | 10 | -0.018804 | -6.059 |
| w16 | 0 | None | 0.0 |
| w17 | 14 | -0.122232 | -16.963 |
| w18 | 23 | -0.125551 | -10.577 |
| w19 | 22 | -0.128554 | -21.783 |
| w21 | 0 | 0.02855 | 0.0 |
| w22 | 0 | 0.057711 | 0.0 |
| w23 | 0 | -0.027775 | 0.0 |
| w24 | 10 | 0.05396 | -5.218 |
| w25 | 18 | -0.023126 | -17.735 |
| w26 | 14 | 0.113862 | 5.435 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | -0.097322 | 0.0 |
| w29 | 1 | 0.010489 | 0.4 |
| w30 | 28 | -0.03401 | 10.461 |
| w31 | 20 | -0.220741 | -2.818 |
| w32 | 32 | -0.063763 | -22.06 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | -0.048632 | -32.54 |
| w23 | 27 | 0.041309 | -8.674 |
| w24 | 28 | -0.025212 | -31.334 |
| w25 | 4 | -0.060655 | -7.948 |
| w26 | 8 | 0.000204 | -4.122 |
| w27 | 17 | -0.024905 | -14.886 |
| w28 | 11 | -0.004008 | -1.215 |
| w29 | 18 | -0.094899 | -10.688 |
| w30 | 7 | -0.034211 | 8.01 |
| w31 | 13 | -0.003486 | 22.51 |
| w32 | 40 | -0.17348 | -26.588 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 6 | 0.005792 | 2.163 |
| w12 | 42 | -0.07323 | 14.708 |
| w13 | 5 | -0.070346 | -26.97 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | -0.076159 | -11.155 |
| w18 | 16 | -0.019909 | -8.073 |
| w19 | 9 | -0.091901 | -19.008 |
| w20 | 10 | -0.005447 | -6.589 |
| w21 | 10 | 0.028366 | -0.898 |
| w22 | 13 | -0.199142 | -13.759 |
| w23 | 12 | -0.035943 | -4.105 |
| w24 | 7 | 0.01937 | -5.052 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | 0.060072 | -3.026 |
| w27 | 2 | -0.080359 | -11.455 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.073424 | 2.699 |
| w30 | 0 | None | 0.0 |
| w31 | 13 | 0.035597 | 5.862 |
| w32 | 6 | 0.008573 | -3.051 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 2 | -0.059501 | -9.997 |
| w26 | 13 | -0.05199 | -15.833 |
| w27 | 13 | -0.118136 | -13.192 |
| w28 | 13 | -0.077852 | -15.908 |
| w29 | 7 | -0.228955 | -18.563 |
| w30 | 11 | 0.007861 | 12.888 |
| w31 | 33 | -0.106927 | 7.725 |
| w32 | 4 | 0.040268 | -0.338 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | 0.012626 | -6.495 |
| w23 | 32 | 0.057154 | 15.638 |
| w24 | 27 | 0.036076 | -7.624 |
| w25 | 0 | None | 0.0 |
| w26 | 18 | 0.075713 | 24.432 |
| w27 | 16 | -0.062194 | -12.342 |
| w28 | 15 | -0.048213 | -4.562 |
| w29 | 15 | -0.072239 | 1.95 |
| w30 | 15 | 0.010442 | 28.152 |
| w31 | 17 | -0.042271 | 16.089 |
| w32 | 22 | -0.073992 | -14.954 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 18 | -0.013776 | -2.481 |
| w21 | 17 | -0.060347 | -9.895 |
| w22 | 22 | 0.073821 | -31.808 |
| w23 | 19 | 0.118553 | 21.476 |
| w24 | 18 | 0.03372 | 4.05 |
| w25 | 6 | 0.021838 | -1.71 |
| w26 | 4 | 0.108376 | 6.859 |
| w27 | 13 | 0.047044 | -6.363 |
| w28 | 2 | 0.01554 | 7.181 |
| w29 | 11 | -0.118651 | -13.858 |
| w30 | 18 | 0.022259 | 17.817 |
| w31 | 26 | -0.161764 | 2.963 |
| w32 | 27 | -0.08861 | -34.435 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.014971 | -1.384 |
| w2 | 1 | 0.030635 | 0.304 |
| w3 | 4 | -0.165857 | -8.73 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 18 | 0.012285 | 0.711 |
| w8 | 25 | -0.07939 | -16.193 |
| w9 | 10 | 0.052589 | 20.406 |
| w10 | 3 | 0.053008 | 0.281 |
| w11 | 0 | None | 0.0 |
| w12 | 23 | 0.007604 | 7.626 |
| w13 | 4 | -0.055182 | -9.862 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 8 | 0.023527 | -1.223 |
| w19 | 20 | -0.079652 | -7.037 |
| w20 | 12 | -0.069624 | -14.072 |
| w21 | 19 | -0.010359 | -9.305 |
| w22 | 4 | 0.03221 | -1.801 |
| w23 | 8 | -0.051119 | -4.026 |
| w24 | 6 | 0.016319 | 1.59 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.075154 | -1.011 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | 0.032103 | 0.66 |
| w31 | 6 | -0.097741 | -9.13 |
| w32 | 15 | 0.054724 | 5.153 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 20 | 0.06963 | 15.954 |
| w22 | 2 | 0.019039 | 0.015 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 28 | 0.005637 | 7.585 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | -0.023165 | 2.113 |

