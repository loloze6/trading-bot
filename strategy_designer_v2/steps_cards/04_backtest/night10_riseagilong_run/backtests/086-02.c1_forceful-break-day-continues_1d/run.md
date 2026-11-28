# Backtest of 086-02.c1_forceful-break-day-continues_1d

- Plan: `../../../../03_test_plan/night10_riseagilong_run/plans/086-02.c1_forceful-break-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.082032 | 0.0 |
| w3 | 2 | 0.143678 | 0.265 |
| w4 | 5 | -0.035558 | 3.757 |
| w5 | 17 | -0.017235 | -6.244 |
| w6 | 10 | 0.135677 | 81.627 |
| w7 | 8 | -0.1048 | -4.001 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | -0.043569 | 9.971 |
| w11 | 6 | 0.024361 | 10.595 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | -0.010791 | -5.925 |
| w14 | 3 | -0.092731 | 0.849 |
| w15 | 12 | -0.023476 | 55.185 |
| w16 | 11 | 0.078525 | 7.588 |
| w17 | 1 | -0.437678 | -12.32 |
| w18 | 5 | 0.035316 | -8.075 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.218894 | 5.37 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.003039 | -0.734 |
| w24 | 0 | None | 0.0 |
| w25 | 4 | -0.019835 | 17.911 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.033028 | 29.296 |
| w28 | 13 | 0.212342 | -7.597 |
| w29 | 5 | -0.053524 | -7.08 |
| w30 | 2 | 0.029313 | 1.392 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 9 | -0.176867 | 1.701 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | -0.077601 | -7.118 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | -0.023479 | -12.683 |
| w14 | 5 | -0.012948 | -1.085 |
| w15 | 8 | -0.06688 | 19.462 |
| w16 | 16 | 0.248315 | 79.216 |
| w17 | 9 | -0.119907 | -40.658 |
| w18 | 4 | 0.022154 | 1.092 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.018448 | -1.984 |
| w21 | 3 | -0.193825 | -7.09 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.039186 | 0.002 |
| w25 | 15 | -0.07639 | -1.455 |
| w26 | 6 | 0.009208 | -0.782 |
| w27 | 12 | -0.034451 | -3.363 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.103544 | -4.375 |
| w30 | 1 | 0.005296 | -3.04 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 6 | -0.096374 | -19.784 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.057209 | -16.418 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.145697 | 3.077 |
| w16 | 15 | -0.024099 | 22.093 |
| w17 | 2 | -0.039738 | -0.947 |
| w18 | 5 | -0.024448 | -7.142 |
| w19 | 4 | -0.034525 | 0.244 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.055461 | 2.729 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.066866 | 6.191 |
| w27 | 4 | -0.024153 | -0.108 |
| w28 | 11 | 0.10315 | 10.804 |
| w29 | 5 | 0.086932 | -8.169 |
| w30 | 17 | 0.14051 | 23.491 |
| w31 | 5 | -0.316899 | -15.712 |
| w32 | 2 | 0.057193 | -13.777 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 6 | -0.051322 | -2.636 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.069724 | 6.967 |
| w28 | 2 | 0.098771 | 7.706 |
| w29 | 4 | 0.090537 | 1.796 |
| w30 | 2 | 0.042553 | 0.03 |
| w31 | 0 | None | 0.0 |
| w32 | 6 | -0.028807 | 1.446 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.033526 | 1.852 |
| w25 | 10 | -0.107555 | 7.742 |
| w26 | 1 | -0.130783 | -14.298 |
| w27 | 9 | 0.132998 | 15.7 |
| w28 | 4 | 0.156747 | 3.304 |
| w29 | 4 | -0.051887 | -2.442 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.073187 | -4.781 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.07761 | 1.452 |
| w25 | 11 | -0.105749 | -7.089 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | -0.095321 | -1.916 |
| w28 | 0 | None | 0.0 |
| w29 | 10 | -0.004609 | -2.42 |
| w30 | 2 | 0.061419 | 1.187 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 1 | -0.008619 | 0.219 |
| w13 | 5 | -0.111513 | -8.007 |
| w14 | 4 | 0.026475 | 3.409 |
| w15 | 9 | -0.053843 | -17.879 |
| w16 | 10 | -0.056026 | 9.009 |
| w17 | 7 | -0.009364 | -7.975 |
| w18 | 2 | 0.083744 | 0.137 |
| w19 | 0 | None | 0.0 |
| w21 | 0 | 0.017954 | 0.0 |
| w22 | 0 | -0.055272 | 0.0 |
| w23 | 4 | -0.156581 | -2.194 |
| w24 | 3 | 0.051128 | -0.398 |
| w25 | 6 | -0.111967 | -18.913 |
| w26 | 0 | -0.010296 | 0.0 |
| w27 | 6 | 0.035494 | 16.901 |
| w28 | 5 | -0.071901 | -5.58 |
| w29 | 4 | 0.084861 | 7.2 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | -0.145765 | -1.827 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.027738 | -10.179 |
| w23 | 3 | -0.116171 | -16.782 |
| w24 | 8 | 0.010956 | -1.483 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | 0.027465 | 12.097 |
| w27 | 11 | 0.041713 | 10.39 |
| w28 | 5 | -0.010132 | 0.539 |
| w29 | 2 | -0.120371 | -6.478 |
| w30 | 2 | 0.010474 | 12.628 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

