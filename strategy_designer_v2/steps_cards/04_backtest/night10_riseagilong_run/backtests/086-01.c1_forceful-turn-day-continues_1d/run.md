# Backtest of 086-01.c1_forceful-turn-day-continues_1d

- Plan: `../../../../03_test_plan/night10_riseagilong_run/plans/086-01.c1_forceful-turn-day-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.082032 | 0.0 |
| w3 | 2 | 0.143678 | 0.859 |
| w4 | 4 | -0.035558 | 2.299 |
| w5 | 20 | -0.017235 | -11.183 |
| w6 | 9 | 0.135677 | 50.306 |
| w7 | 6 | -0.1048 | 0.499 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | -0.043569 | 1.256 |
| w11 | 7 | 0.024361 | 0.158 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.010791 | -5.51 |
| w14 | 3 | -0.092731 | 1.489 |
| w15 | 11 | -0.023476 | 26.505 |
| w16 | 16 | 0.078525 | 5.209 |
| w17 | 1 | -0.437678 | -9.284 |
| w18 | 5 | 0.035316 | -4.668 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | 0.218894 | 4.05 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.003039 | 0.382 |
| w24 | 0 | None | 0.0 |
| w25 | 4 | -0.019835 | 2.308 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | 0.033028 | 24.034 |
| w28 | 13 | 0.212342 | 10.828 |
| w29 | 5 | -0.053524 | -1.522 |
| w30 | 2 | 0.029313 | 0.097 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | -0.176867 | 2.442 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | -0.077601 | -10.987 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.023479 | -10.033 |
| w14 | 5 | -0.012948 | -1.351 |
| w15 | 8 | -0.06688 | 5.833 |
| w16 | 17 | 0.248315 | 64.262 |
| w17 | 9 | -0.119907 | -14.018 |
| w18 | 5 | 0.022154 | -4.583 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.018448 | 0.761 |
| w21 | 3 | -0.193825 | -4.949 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.039186 | -1.795 |
| w25 | 16 | -0.07639 | -6.241 |
| w26 | 5 | 0.009208 | 0.165 |
| w27 | 12 | -0.034451 | 2.66 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.103544 | 6.991 |
| w30 | 1 | 0.005296 | -0.879 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 6 | -0.096374 | -11.866 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.057209 | -8.594 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | -0.145697 | -5.822 |
| w16 | 16 | -0.024099 | 7.289 |
| w17 | 2 | -0.039738 | -0.226 |
| w18 | 4 | -0.024448 | -12.03 |
| w19 | 3 | -0.034525 | 0.509 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.055461 | 9.408 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.066866 | -1.617 |
| w27 | 4 | -0.024153 | -6.317 |
| w28 | 9 | 0.10315 | 8.018 |
| w29 | 6 | 0.086932 | -11.193 |
| w30 | 18 | 0.14051 | 22.45 |
| w31 | 5 | -0.316899 | -14.129 |
| w32 | 2 | 0.057193 | -19.126 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | -0.051322 | -6.293 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.069724 | 0.19 |
| w28 | 2 | 0.098771 | 4.331 |
| w29 | 4 | 0.090537 | 3.974 |
| w30 | 2 | 0.042553 | -0.063 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.028807 | 5.398 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.033526 | -0.28 |
| w25 | 14 | -0.107555 | 11.091 |
| w26 | 1 | -0.130783 | -7.442 |
| w27 | 8 | 0.132998 | 13.102 |
| w28 | 4 | 0.156747 | 11.172 |
| w29 | 3 | -0.051887 | 1.573 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.073187 | -3.544 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.07761 | 9.503 |
| w25 | 13 | -0.105749 | -10.398 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | -0.095321 | -0.145 |
| w28 | 0 | None | 0.0 |
| w29 | 11 | -0.004609 | 1.051 |
| w30 | 2 | 0.061419 | 0.253 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 1 | -0.008619 | -1.064 |
| w13 | 5 | -0.111513 | -8.652 |
| w14 | 4 | 0.026475 | 4.55 |
| w15 | 8 | -0.053843 | -6.696 |
| w16 | 13 | -0.056026 | 1.522 |
| w17 | 6 | -0.009364 | -0.424 |
| w18 | 2 | 0.083744 | 0.194 |
| w19 | 0 | None | 0.0 |
| w21 | 0 | 0.017954 | 0.0 |
| w22 | 0 | -0.055272 | 0.0 |
| w23 | 5 | -0.156581 | -2.881 |
| w24 | 2 | 0.051128 | 2.909 |
| w25 | 5 | -0.111967 | -8.445 |
| w26 | 0 | -0.010296 | 0.0 |
| w27 | 9 | 0.035494 | 3.462 |
| w28 | 4 | -0.071901 | -8.025 |
| w29 | 4 | 0.084861 | -2.082 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | -0.145765 | -2.359 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.027738 | -2.892 |
| w23 | 3 | -0.116171 | -13.808 |
| w24 | 8 | 0.010956 | 16.556 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | 0.027465 | 9.525 |
| w27 | 11 | 0.041713 | 15.155 |
| w28 | 6 | -0.010132 | -0.195 |
| w29 | 2 | -0.120371 | -7.506 |
| w30 | 2 | 0.010474 | 4.133 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

