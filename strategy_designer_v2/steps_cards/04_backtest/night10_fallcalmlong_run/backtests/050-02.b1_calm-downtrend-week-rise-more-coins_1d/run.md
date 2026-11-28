# Backtest of 050-02.b1_calm-downtrend-week-rise-more-coins_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/050-02.b1_calm-downtrend-week-rise-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 11 | 0.05483 | 24.515 |
| w14 | 3 | -0.060709 | -1.386 |
| w15 | 4 | 0.012465 | 3.73 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.05305 | 16.577 |
| w18 | 11 | -0.042395 | -5.382 |
| w19 | 20 | -0.008106 | -5.438 |
| w20 | 5 | 0.021112 | 0.039 |
| w21 | 4 | -0.121352 | -4.347 |
| w22 | 3 | -0.015407 | 2.396 |
| w23 | 10 | -0.018387 | 3.581 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.062739 | -10.593 |
| w27 | 11 | -0.089557 | -5.973 |
| w28 | 7 | 0.240297 | 13.71 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | -0.129967 | -2.955 |
| w31 | 17 | -0.066127 | -3.521 |
| w32 | 4 | 0.038339 | 0.997 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 15 | 0.113854 | 19.499 |
| w8 | 18 | -0.003291 | -10.715 |
| w9 | 5 | -0.022295 | -0.812 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.044283 | -1.02 |
| w12 | 15 | 0.113809 | 12.728 |
| w13 | 11 | -0.014012 | 9.369 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.060635 | -3.814 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.042109 | 3.584 |
| w18 | 0 | None | 0.0 |
| w19 | 15 | 0.072791 | 1.344 |
| w20 | 0 | None | 0.0 |
| w21 | 12 | 0.015864 | 7.121 |
| w22 | 2 | -0.017792 | 1.55 |
| w23 | 3 | -0.094857 | -9.684 |
| w24 | 7 | 0.025206 | 0.106 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | 0.003637 | 1.275 |
| w28 | 5 | -0.161266 | -10.644 |
| w29 | 0 | None | 0.0 |
| w30 | 15 | 0.010298 | -4.966 |
| w31 | 15 | 0.044161 | 5.645 |
| w32 | 15 | -0.007074 | 1.006 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 10 | 0.089122 | 2.178 |
| w11 | 1 | -0.017728 | 0.128 |
| w12 | 20 | -0.031812 | -9.456 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.024209 | -3.008 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.092826 | 19.235 |
| w18 | 2 | -0.022621 | 1.106 |
| w19 | 13 | 0.058599 | 8.658 |
| w20 | 14 | 0.015659 | 1.017 |
| w21 | 14 | -0.087037 | -7.133 |
| w22 | 14 | 0.009214 | 0.05 |
| w23 | 10 | -0.080428 | -10.577 |
| w24 | 16 | 0.023144 | 0.991 |
| w25 | 0 | None | 0.0 |
| w26 | 11 | 0.035278 | 10.23 |
| w27 | 5 | 0.192348 | 18.244 |
| w28 | 2 | 0.180561 | 2.449 |
| w29 | 6 | -0.112189 | -11.686 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 11 | 0.047225 | 2.999 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 13 | 0.180462 | 14.662 |
| w24 | 8 | 0.075051 | 8.04 |
| w25 | 6 | 0.056719 | 4.903 |
| w26 | 9 | 0.117717 | 15.484 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 7.426 |
| w30 | 9 | 0.064187 | 0.606 |
| w31 | 16 | 0.064815 | -4.411 |
| w32 | 12 | 0.010443 | 2.557 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.009015 | 5.007 |
| w23 | 23 | 0.008397 | -12.386 |
| w24 | 12 | -0.127653 | -14.225 |
| w25 | 0 | None | 0.0 |
| w26 | 15 | -0.088049 | -10.091 |
| w27 | 16 | -0.02289 | 0.151 |
| w28 | 11 | 0.056847 | 4.227 |
| w29 | 10 | 0.037295 | 3.488 |
| w30 | 9 | -0.032141 | -12.109 |
| w31 | 7 | 0.002686 | -3.427 |
| w32 | 11 | -0.069827 | -10.312 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | -0.040343 | -4.386 |
| w21 | 15 | -0.029308 | 4.186 |
| w22 | 26 | 0.20658 | 38.279 |
| w23 | 14 | -0.051836 | -11.786 |
| w24 | 7 | -0.080398 | -5.568 |
| w25 | 7 | 0.001274 | 1.65 |
| w26 | 2 | -0.082249 | -0.54 |
| w27 | 9 | -0.054574 | -0.153 |
| w28 | 2 | -0.052464 | -3.263 |
| w29 | 3 | 0.067594 | 8.599 |
| w30 | 9 | -0.089194 | -8.447 |
| w31 | 18 | 0.033975 | -1.13 |
| w32 | 16 | 0.039794 | 32.716 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 14 | -0.005341 | -3.098 |
| w21 | 1 | -0.045033 | -0.024 |
| w22 | 12 | 0.083645 | 2.65 |
| w23 | 17 | 0.042925 | -8.699 |
| w24 | 6 | -0.041635 | 0.087 |
| w25 | 10 | 0.009233 | -1.659 |
| w26 | 24 | 0.041053 | -5.991 |
| w27 | 8 | -0.050386 | -3.308 |
| w28 | 0 | None | 0.0 |
| w29 | 14 | 0.282886 | 32.812 |
| w30 | 19 | -0.158257 | -22.454 |
| w31 | 12 | 0.017794 | 11.127 |
| w32 | 15 | 0.009362 | -4.238 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | 0.004931 | -0.018 |
| w12 | 28 | -0.003684 | -5.708 |
| w13 | 4 | 0.108273 | 19.37 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.04284 | 9.372 |
| w18 | 10 | 0.003551 | 4.292 |
| w19 | 8 | -0.122566 | -6.283 |
| w20 | 16 | -0.011813 | 2.527 |
| w21 | 6 | -0.056981 | -0.735 |
| w22 | 10 | 0.121202 | 4.6 |
| w23 | 2 | -0.169013 | -1.226 |
| w24 | 6 | 0.054594 | 0.523 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.09198 | -0.269 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | 0.070228 | 11.269 |
| w29 | 0 | -0.007473 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 10 | -0.03178 | -2.968 |
| w32 | 6 | 0.031854 | 5.088 |

