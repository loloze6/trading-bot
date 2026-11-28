# Backtest of 086-02_first-up-after-deep-down-run_1d

- Plan: `../../../../03_test_plan/night10_riseagilong_run/plans/086-02_first-up-after-deep-down-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | 0.041419 | 0.0 |
| w3 | 2 | 0.143678 | 0.51 |
| w4 | 5 | -0.051309 | 13.685 |
| w5 | 11 | -0.000489 | -5.489 |
| w6 | 8 | 0.037751 | 44.643 |
| w7 | 10 | -0.027483 | -12.131 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | -0.042144 | 24.664 |
| w11 | 6 | 0.184305 | 38.093 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.025796 | -9.239 |
| w14 | 4 | -0.130783 | -2.211 |
| w15 | 10 | -0.023857 | 106.878 |
| w16 | 16 | 0.071554 | 9.136 |
| w17 | 3 | -0.252184 | -36.295 |
| w18 | 6 | 0.01703 | -19.721 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | 0.107553 | 6.592 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.002465 | -2.593 |
| w24 | 0 | None | 0.0 |
| w25 | 7 | -0.081018 | 2.58 |
| w26 | 0 | None | 0.0 |
| w27 | 12 | 0.035201 | 78.105 |
| w28 | 12 | 0.1793 | -5.824 |
| w29 | 4 | -0.050074 | -15.908 |
| w30 | 2 | 0.029313 | 2.38 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | -0.174819 | -6.25 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | -0.064636 | -20.333 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.026341 | -40.858 |
| w14 | 6 | -0.034043 | -7.322 |
| w15 | 7 | -0.199347 | 30.746 |
| w16 | 19 | 0.202019 | 132.898 |
| w17 | 8 | -0.196335 | -42.353 |
| w18 | 2 | 0.040793 | 8.299 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.00855 | -5.13 |
| w21 | 3 | -0.156527 | -8.957 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.017178 | 6.675 |
| w25 | 16 | -0.073395 | -12.095 |
| w26 | 5 | 0.01263 | -1.576 |
| w27 | 11 | -0.053342 | -6.283 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.049126 | -5.556 |
| w30 | 2 | 0.005296 | -9.083 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 6 | -0.06053 | -23.511 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | -0.05171 | -26.85 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.152125 | 10.993 |
| w16 | 17 | 0.025501 | 52.537 |
| w17 | 2 | -0.039738 | -1.987 |
| w18 | 5 | -0.086115 | -9.142 |
| w19 | 4 | -0.026876 | 2.198 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.020473 | 3.384 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | -0.161903 | 2.93 |
| w27 | 4 | -0.102389 | -2.818 |
| w28 | 10 | 0.079078 | 12.049 |
| w29 | 6 | 0.108901 | -5.659 |
| w30 | 18 | 0.091908 | 36.009 |
| w31 | 6 | -0.153231 | -19.551 |
| w32 | 2 | 0.057193 | -13.777 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | -0.069037 | -5.175 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.078742 | 12.975 |
| w28 | 2 | 0.098771 | 16.087 |
| w29 | 6 | 0.092599 | 1.764 |
| w30 | 2 | 0.042553 | 0.057 |
| w31 | 0 | None | 0.0 |
| w32 | 9 | 0.098311 | 13.842 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.079069 | 16.831 |
| w25 | 10 | -0.115871 | -10.909 |
| w26 | 1 | -0.130783 | -14.298 |
| w27 | 9 | 0.070895 | 21.752 |
| w28 | 4 | 0.159099 | 8.823 |
| w29 | 4 | -0.0122 | 1.751 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 6 | -0.049892 | -19.532 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.085053 | -0.115 |
| w25 | 9 | -0.117129 | -19.839 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | -0.117667 | 20.912 |
| w28 | 0 | None | 0.0 |
| w29 | 13 | -0.021824 | -18.793 |
| w30 | 2 | 0.061419 | 3.682 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 2 | -0.008619 | 1.595 |
| w13 | 4 | -0.091565 | -24.762 |
| w14 | 4 | -0.047931 | 0.014 |
| w15 | 9 | -0.041847 | -13.346 |
| w16 | 9 | -0.122038 | 16.27 |
| w17 | 7 | -0.015831 | -8.254 |
| w18 | 2 | 0.083744 | 0.743 |
| w19 | 0 | None | 0.0 |
| w21 | 0 | 0.068654 | 0.0 |
| w22 | 0 | -0.045376 | 0.0 |
| w23 | 5 | -0.124425 | -5.781 |
| w24 | 6 | 0.019456 | -10.884 |
| w25 | 6 | -0.068061 | -21.48 |
| w26 | 3 | -0.023667 | 3.318 |
| w27 | 8 | -0.003977 | 40.365 |
| w28 | 5 | -0.110324 | -4.592 |
| w29 | 4 | 0.07118 | 5.899 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.145765 | -5.946 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 0 | None | 0.0 |
| w22 | 7 | -0.059603 | -27.105 |
| w23 | 4 | -0.276296 | -26.754 |
| w24 | 9 | 0.030471 | -6.639 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | 0.044409 | 15.246 |
| w27 | 13 | 0.034791 | 11.261 |
| w28 | 3 | -0.114167 | -2.0 |
| w29 | 2 | -0.120371 | -6.478 |
| w30 | 2 | 0.010474 | 12.628 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

