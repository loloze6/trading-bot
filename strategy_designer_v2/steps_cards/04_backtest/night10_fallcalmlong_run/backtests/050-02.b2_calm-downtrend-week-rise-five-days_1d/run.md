# Backtest of 050-02.b2_calm-downtrend-week-rise-five-days_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/050-02.b2_calm-downtrend-week-rise-five-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 9 | 0.05483 | 30.42 |
| w14 | 3 | -0.060709 | -1.439 |
| w15 | 4 | 0.012465 | 3.73 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.05305 | 18.506 |
| w18 | 10 | -0.042395 | 0.42 |
| w19 | 18 | -0.008106 | -13.189 |
| w20 | 5 | 0.021112 | 4.315 |
| w21 | 4 | -0.121352 | -6.449 |
| w22 | 3 | -0.015407 | 5.826 |
| w23 | 11 | -0.018387 | 22.017 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.062739 | -10.275 |
| w27 | 12 | -0.089557 | -8.639 |
| w28 | 6 | 0.240297 | 10.688 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.129967 | -0.629 |
| w31 | 12 | -0.066127 | -3.542 |
| w32 | 4 | 0.038339 | -0.252 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 15 | 0.113854 | 21.891 |
| w8 | 16 | -0.003291 | -14.928 |
| w9 | 5 | -0.022295 | -6.217 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.044283 | -3.612 |
| w12 | 13 | 0.113809 | 21.077 |
| w13 | 8 | -0.014012 | 11.337 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.060635 | -0.758 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.042109 | 9.022 |
| w18 | 0 | None | 0.0 |
| w19 | 15 | 0.072791 | -1.504 |
| w20 | 0 | None | 0.0 |
| w21 | 11 | 0.015864 | 10.595 |
| w22 | 2 | -0.017792 | 5.444 |
| w23 | 3 | -0.094857 | -9.684 |
| w24 | 8 | 0.025206 | -9.618 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.003637 | -3.388 |
| w28 | 5 | -0.161266 | -14.34 |
| w29 | 0 | None | 0.0 |
| w30 | 14 | 0.010298 | -3.451 |
| w31 | 15 | 0.044161 | 11.672 |
| w32 | 12 | -0.007074 | 2.201 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 7 | 0.089122 | 2.874 |
| w11 | 2 | -0.017728 | -1.97 |
| w12 | 21 | -0.031812 | -5.966 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 13 | -0.024209 | 0.605 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.092826 | 21.206 |
| w18 | 2 | -0.022621 | 1.892 |
| w19 | 12 | 0.058599 | 7.472 |
| w20 | 12 | 0.015659 | -0.336 |
| w21 | 10 | -0.087037 | -7.833 |
| w22 | 13 | 0.009214 | 2.827 |
| w23 | 7 | -0.080428 | -7.762 |
| w24 | 13 | 0.023144 | 1.494 |
| w25 | 0 | None | 0.0 |
| w26 | 10 | 0.035278 | 13.279 |
| w27 | 6 | 0.192348 | 19.551 |
| w28 | 2 | 0.180561 | 2.449 |
| w29 | 4 | -0.112189 | -4.343 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 10 | 0.047225 | 4.939 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 13 | 0.180462 | 10.075 |
| w24 | 8 | 0.075051 | 6.907 |
| w25 | 6 | 0.056719 | 11.7 |
| w26 | 10 | 0.117717 | 14.815 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 6.592 |
| w30 | 7 | 0.064187 | -2.211 |
| w31 | 15 | 0.064815 | -20.223 |
| w32 | 12 | 0.010443 | 1.827 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.009015 | 5.041 |
| w23 | 21 | 0.008397 | -10.241 |
| w24 | 16 | -0.127653 | -13.415 |
| w25 | 0 | None | 0.0 |
| w26 | 12 | -0.088049 | -13.393 |
| w27 | 15 | -0.02289 | 2.855 |
| w28 | 9 | 0.056847 | 2.462 |
| w29 | 10 | 0.037295 | 2.741 |
| w30 | 7 | -0.032141 | -12.826 |
| w31 | 7 | 0.002686 | -4.368 |
| w32 | 11 | -0.069827 | -9.568 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 11 | -0.040343 | -2.771 |
| w21 | 14 | -0.029308 | 16.152 |
| w22 | 20 | 0.20658 | 22.581 |
| w23 | 13 | -0.051836 | -11.159 |
| w24 | 8 | -0.080398 | -6.29 |
| w25 | 8 | 0.001274 | 6.186 |
| w26 | 2 | -0.082249 | -0.317 |
| w27 | 9 | -0.054574 | 8.868 |
| w28 | 2 | -0.052464 | -4.828 |
| w29 | 4 | 0.067594 | 8.972 |
| w30 | 8 | -0.089194 | -6.309 |
| w31 | 17 | 0.033975 | -7.088 |
| w32 | 14 | 0.039794 | 29.194 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 14 | -0.005341 | 4.12 |
| w21 | 1 | -0.045033 | -0.024 |
| w22 | 12 | 0.083645 | -1.354 |
| w23 | 14 | 0.042925 | -12.039 |
| w24 | 7 | -0.041635 | -1.201 |
| w25 | 10 | 0.009233 | 13.089 |
| w26 | 18 | 0.041053 | -10.563 |
| w27 | 9 | -0.050386 | -2.847 |
| w28 | 0 | None | 0.0 |
| w29 | 10 | 0.282886 | 47.982 |
| w30 | 19 | -0.158257 | -36.099 |
| w31 | 12 | 0.017794 | 5.213 |
| w32 | 14 | 0.009362 | -6.393 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | 0.004931 | -0.147 |
| w12 | 26 | -0.003684 | -1.577 |
| w13 | 4 | 0.108273 | 18.828 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.04284 | 16.222 |
| w18 | 12 | 0.003551 | 8.053 |
| w19 | 9 | -0.122566 | -13.859 |
| w20 | 15 | -0.011813 | 4.402 |
| w21 | 6 | -0.056981 | -5.313 |
| w22 | 10 | 0.121202 | 4.048 |
| w23 | 2 | -0.169013 | -1.226 |
| w24 | 6 | 0.054594 | -3.673 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.09198 | 2.165 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | 0.070228 | 9.39 |
| w29 | 0 | -0.007473 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 10 | -0.03178 | -3.773 |
| w32 | 6 | 0.031854 | 6.734 |

