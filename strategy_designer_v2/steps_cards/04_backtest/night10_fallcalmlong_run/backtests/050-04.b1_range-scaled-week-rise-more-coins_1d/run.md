# Backtest of 050-04.b1_range-scaled-week-rise-more-coins_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/050-04.b1_range-scaled-week-rise-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 11 | 0.057412 | 27.014 |
| w14 | 3 | -0.062432 | -1.307 |
| w15 | 4 | 0.01241 | 3.731 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.054318 | 16.413 |
| w18 | 11 | -0.037365 | -4.588 |
| w19 | 21 | -0.004483 | -4.538 |
| w20 | 5 | 0.019465 | -0.176 |
| w21 | 2 | -0.118332 | -4.104 |
| w22 | 3 | -0.015734 | 2.262 |
| w23 | 10 | -0.019099 | 3.316 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.06302 | -10.659 |
| w27 | 11 | -0.090168 | -5.724 |
| w28 | 7 | 0.226038 | 12.36 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | -0.129813 | -2.593 |
| w31 | 17 | -0.055349 | -3.173 |
| w32 | 4 | 0.037241 | 0.821 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 14 | 0.121099 | 21.938 |
| w8 | 20 | 0.005793 | -9.783 |
| w9 | 5 | -0.022006 | -0.81 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.044496 | -0.958 |
| w12 | 16 | 0.11057 | 11.876 |
| w13 | 11 | -0.015531 | 10.764 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.061737 | -3.814 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.042109 | 3.584 |
| w18 | 0 | None | 0.0 |
| w19 | 15 | 0.068929 | 0.691 |
| w20 | 0 | None | 0.0 |
| w21 | 12 | 0.002429 | 4.325 |
| w22 | 2 | -0.017666 | 1.394 |
| w23 | 3 | -0.094759 | -9.684 |
| w24 | 7 | 0.02143 | 0.307 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | 0.00257 | 1.131 |
| w28 | 5 | -0.163654 | -8.554 |
| w29 | 0 | None | 0.0 |
| w30 | 13 | 0.01187 | -4.149 |
| w31 | 15 | 0.039784 | 4.953 |
| w32 | 15 | 0.000506 | 1.974 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 10 | 0.088345 | 2.08 |
| w11 | 1 | -0.017728 | 0.109 |
| w12 | 20 | -0.032374 | -9.283 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.032377 | -3.743 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.090594 | 17.195 |
| w18 | 2 | -0.022874 | 1.127 |
| w19 | 12 | 0.045649 | 6.077 |
| w20 | 15 | 0.017308 | 1.413 |
| w21 | 14 | -0.098549 | -7.169 |
| w22 | 14 | 0.011905 | 0.132 |
| w23 | 10 | -0.08332 | -10.297 |
| w24 | 14 | 0.021615 | 0.386 |
| w25 | 0 | None | 0.0 |
| w26 | 11 | 0.029516 | 9.223 |
| w27 | 5 | 0.190425 | 17.628 |
| w28 | 2 | 0.180561 | 1.872 |
| w29 | 6 | -0.110977 | -9.022 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | 0.045688 | 3.301 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 11 | 0.199685 | 17.312 |
| w24 | 8 | 0.072058 | 7.997 |
| w25 | 8 | 0.054741 | 5.162 |
| w26 | 9 | 0.12387 | 15.318 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 7.317 |
| w30 | 9 | 0.059046 | 0.697 |
| w31 | 17 | 0.065562 | -3.395 |
| w32 | 12 | 0.007304 | 2.026 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.017147 | 5.601 |
| w23 | 23 | 0.008343 | -11.964 |
| w24 | 10 | -0.130995 | -15.937 |
| w25 | 0 | None | 0.0 |
| w26 | 13 | -0.080962 | -9.728 |
| w27 | 12 | -0.0287 | -1.051 |
| w28 | 11 | 0.05653 | 4.18 |
| w29 | 10 | 0.03734 | 3.117 |
| w30 | 7 | -0.026424 | -11.95 |
| w31 | 7 | -0.004264 | -3.589 |
| w32 | 10 | -0.078164 | -9.04 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | -0.033342 | -4.05 |
| w21 | 13 | -0.029666 | 5.397 |
| w22 | 24 | 0.210999 | 38.306 |
| w23 | 14 | -0.047974 | -10.933 |
| w24 | 6 | -0.083671 | -5.583 |
| w25 | 7 | 0.002656 | 2.506 |
| w26 | 2 | -0.082485 | -0.494 |
| w27 | 9 | -0.055946 | 0.04 |
| w28 | 2 | -0.049878 | -3.102 |
| w29 | 4 | 0.056414 | 7.02 |
| w30 | 9 | -0.09294 | -8.344 |
| w31 | 16 | 0.036453 | -0.282 |
| w32 | 16 | 0.043222 | 33.873 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 15 | -0.008149 | -3.238 |
| w21 | 1 | -0.045033 | -0.021 |
| w22 | 12 | 0.080306 | 0.437 |
| w23 | 15 | 0.03911 | -8.868 |
| w24 | 6 | -0.041123 | 0.024 |
| w25 | 11 | 0.013386 | -1.222 |
| w26 | 22 | 0.042472 | -5.791 |
| w27 | 8 | -0.05023 | -3.333 |
| w28 | 0 | None | 0.0 |
| w29 | 14 | 0.28477 | 33.69 |
| w30 | 19 | -0.16149 | -22.864 |
| w31 | 13 | 0.023629 | 13.766 |
| w32 | 15 | 0.023308 | -2.966 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | 0.005303 | -0.017 |
| w12 | 26 | -0.008285 | -5.623 |
| w13 | 4 | 0.110492 | 19.184 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.044156 | 9.49 |
| w18 | 11 | 0.003008 | 3.563 |
| w19 | 8 | -0.117295 | -6.967 |
| w20 | 16 | -0.00841 | 2.335 |
| w21 | 6 | -0.057867 | -0.528 |
| w22 | 12 | 0.120109 | 4.095 |
| w23 | 2 | -0.169013 | -1.502 |
| w24 | 6 | 0.053716 | 0.481 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.092289 | -0.226 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | 0.067882 | 10.64 |
| w29 | 0 | -0.007473 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 8 | -0.032233 | -2.668 |
| w32 | 6 | 0.023529 | 3.813 |

