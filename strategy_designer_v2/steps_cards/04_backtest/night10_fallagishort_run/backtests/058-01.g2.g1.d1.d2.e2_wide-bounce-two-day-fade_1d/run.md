# Backtest of 058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade_1d

- Plan: `../../../../03_test_plan/night10_fallagishort_run/plans/058-01.g2.g1.d1.d2.e2_wide-bounce-two-day-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 4 | 0.093128 | -0.643 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.039481 | -0.967 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.01065 | 1.311 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | 0.131092 | -1.342 |
| w21 | 5 | -0.018122 | -1.116 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.054419 | 0.208 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.114949 | -5.287 |
| w27 | 0 | None | 0.0 |
| w28 | 8 | 0.018638 | 1.774 |
| w29 | 0 | None | 0.0 |
| w30 | 1 | 0.087131 | -3.017 |
| w31 | 6 | 0.015613 | -0.121 |
| w32 | 7 | 0.162986 | 13.955 |

- AVAXUSD: 7 of 32 windows run. 25 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days); w20, w21, w22, w23, w24, w25 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 14 | -0.030923 | -1.465 |
| w27 | 0 | None | 0.0 |
| w28 | 20 | 0.080135 | 3.468 |
| w29 | 1 | 0.040983 | 1.228 |
| w30 | 6 | -0.089825 | -5.924 |
| w31 | 6 | -0.017543 | -1.457 |
| w32 | 1 | 0.058846 | -0.002 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 4 | 0.025396 | 0.291 |
| w12 | 1 | 0.050092 | 2.915 |
| w13 | 10 | 0.013435 | -3.793 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.069258 | 0.284 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | 0.077613 | 2.458 |
| w20 | 10 | -0.027262 | -13.764 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.082713 | -3.271 |
| w25 | 10 | 0.026656 | 1.499 |
| w26 | 1 | 0.017314 | -0.959 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.130193 | -2.409 |
| w30 | 2 | 0.00706 | -0.658 |
| w31 | 8 | -0.065058 | -1.855 |
| w32 | 6 | 0.044068 | 0.246 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 2 | 0.09869 | 1.508 |
| w26 | 9 | 0.063617 | -8.85 |
| w27 | 1 | 0.134121 | -0.202 |
| w28 | 16 | 0.031968 | -4.552 |
| w29 | 0 | None | 0.0 |
| w30 | 15 | -0.008702 | 2.515 |
| w31 | 4 | 0.047041 | 3.839 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | 0.021939 | -4.672 |
| w27 | 1 | 0.12984 | 1.185 |
| w28 | 12 | 0.035191 | 6.695 |
| w29 | 0 | None | 0.0 |
| w30 | 16 | -0.074852 | -9.211 |
| w31 | 7 | 0.009245 | 0.467 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | 0.002934 | -1.771 |
| w21 | 1 | 0.006136 | -1.9 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 15 | -0.090612 | -9.381 |
| w27 | 0 | None | 0.0 |
| w28 | 15 | 0.06943 | 5.933 |
| w29 | 0 | None | 0.0 |
| w30 | 6 | -0.039916 | -2.136 |
| w31 | 5 | 0.009913 | -1.946 |
| w32 | 0 | None | 0.0 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 2 | 0.076297 | 0.916 |
| w26 | 8 | 0.10953 | -3.911 |
| w27 | 0 | None | 0.0 |
| w28 | 13 | -0.057424 | -3.167 |
| w29 | 0 | None | 0.0 |
| w30 | 14 | -0.192788 | -30.094 |
| w31 | 12 | 0.032481 | 4.424 |
| w32 | 6 | 0.049129 | 1.896 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 5 | 0.05794 | -3.599 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | 0.143656 | 18.346 |
| w10 | 1 | 0.096647 | -0.259 |
| w11 | 3 | -0.005647 | -0.341 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | 0.115503 | 1.075 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.009055 | -0.149 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | -0.013571 | 2.873 |
| w18 | 3 | 0.02462 | 0.833 |
| w19 | 0 | None | 0.0 |
| w20 | 16 | 0.067368 | 12.387 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.058062 | -2.053 |
| w24 | 2 | -0.135216 | -3.846 |
| w25 | 0 | None | 0.0 |
| w26 | 12 | 0.050718 | -5.408 |
| w27 | 0 | None | 0.0 |
| w28 | 11 | 0.078933 | -3.461 |
| w29 | 0 | None | 0.0 |
| w30 | 16 | -0.042569 | -3.922 |
| w31 | 4 | -0.040448 | -0.986 |
| w32 | 0 | None | 0.0 |

