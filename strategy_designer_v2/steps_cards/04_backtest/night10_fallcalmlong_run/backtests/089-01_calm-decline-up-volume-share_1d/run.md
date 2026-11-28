# Backtest of 089-01_calm-decline-up-volume-share_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/089-01_calm-decline-up-volume-share_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 5 | -0.009313 | 9.364 |
| w14 | 5 | -0.035604 | -0.641 |
| w15 | 11 | 0.026656 | 5.183 |
| w16 | 0 | None | 0.0 |
| w17 | 14 | 0.027127 | 18.147 |
| w18 | 6 | 0.132116 | 1.569 |
| w19 | 9 | -0.149541 | -8.866 |
| w20 | 5 | 0.010813 | -3.802 |
| w21 | 8 | -0.102546 | -9.092 |
| w22 | 8 | 0.067028 | 1.79 |
| w23 | 6 | 0.004782 | -13.842 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | 0.004667 | -0.353 |
| w27 | 8 | 0.015942 | -2.36 |
| w28 | 10 | -0.038632 | 5.332 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.128842 | -3.26 |
| w31 | 16 | -0.034004 | -6.443 |
| w32 | 8 | -0.088958 | -14.837 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 11 | 0.082303 | 11.732 |
| w8 | 15 | 0.166933 | 11.12 |
| w9 | 9 | 0.066891 | -3.072 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | -0.027269 | 0.0 |
| w12 | 3 | -0.023778 | -7.255 |
| w13 | 6 | 0.001808 | 5.352 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.049694 | 0.429 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.020562 | -0.183 |
| w19 | 5 | 0.168467 | 3.041 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.007082 | 2.767 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.081929 | 1.747 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | -0.099957 | -8.65 |
| w28 | 9 | 0.048803 | -13.446 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | -0.124052 | -5.394 |
| w31 | 11 | -0.024721 | -1.268 |
| w32 | 8 | 0.008309 | 1.946 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 23 | -0.039569 | -1.854 |
| w11 | 3 | -0.127122 | -2.424 |
| w12 | 15 | -0.215089 | -24.109 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.081071 | -1.321 |
| w15 | 7 | -0.019527 | -6.011 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.094477 | 15.737 |
| w18 | 0 | None | 0.0 |
| w19 | 20 | -0.074185 | -8.598 |
| w20 | 5 | -0.05761 | -1.965 |
| w21 | 18 | -0.032882 | -6.511 |
| w22 | 16 | 0.001084 | 8.285 |
| w23 | 13 | 0.013209 | -14.556 |
| w24 | 17 | 0.028372 | 6.176 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.103836 | -2.513 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | 0.180561 | 1.761 |
| w29 | 5 | -0.105583 | -6.122 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | 0.041338 | -1.576 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 17 | -0.031579 | -8.561 |
| w24 | 8 | 0.114911 | 20.28 |
| w25 | 3 | 0.059107 | 14.866 |
| w26 | 11 | 0.034592 | -0.856 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 14.987 |
| w30 | 7 | -0.123867 | -13.619 |
| w31 | 14 | 0.074119 | 0.855 |
| w32 | 2 | 0.021058 | 9.873 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 7 | 0.017302 | 5.0 |
| w23 | 21 | 0.129517 | -2.918 |
| w24 | 5 | -0.144794 | -4.499 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.057538 | -8.72 |
| w27 | 10 | 0.044775 | 3.175 |
| w28 | 15 | 0.073537 | 3.902 |
| w29 | 6 | -0.000158 | -1.836 |
| w30 | 4 | -0.009587 | -8.611 |
| w31 | 9 | 0.00776 | -8.306 |
| w32 | 5 | -0.034343 | -2.583 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | 0.029183 | -2.331 |
| w21 | 3 | 0.035657 | 0.649 |
| w22 | 12 | 0.144399 | 20.305 |
| w23 | 10 | -0.126488 | -11.298 |
| w24 | 11 | -0.097492 | -6.752 |
| w25 | 5 | 0.00065 | 16.923 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | 0.005176 | 7.446 |
| w28 | 0 | -0.035978 | 0.0 |
| w29 | 3 | -0.015293 | 3.727 |
| w30 | 1 | -0.035641 | -1.308 |
| w31 | 22 | -0.040163 | -6.439 |
| w32 | 11 | -0.033318 | -4.483 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 19 | 0.034756 | 2.326 |
| w21 | 2 | -0.006762 | -0.085 |
| w22 | 7 | 0.059424 | -3.324 |
| w23 | 11 | -0.065547 | -7.118 |
| w24 | 15 | -0.021733 | -6.977 |
| w25 | 8 | 0.04632 | 11.018 |
| w26 | 4 | 0.002978 | -4.06 |
| w27 | 10 | 0.022991 | 7.128 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.448973 | 42.563 |
| w30 | 9 | -0.115201 | -13.972 |
| w31 | 25 | -0.040356 | -0.137 |
| w32 | 22 | -0.05502 | -12.562 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | -0.020376 | -0.111 |
| w12 | 13 | -0.042967 | -1.815 |
| w13 | 4 | 0.078447 | 2.418 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.017318 | 4.418 |
| w18 | 14 | 0.059049 | 2.34 |
| w19 | 6 | -0.11576 | -16.99 |
| w20 | 13 | 0.034443 | 4.978 |
| w21 | 4 | 0.02987 | -1.458 |
| w22 | 9 | 0.051456 | 1.558 |
| w23 | 2 | -0.169013 | -0.907 |
| w24 | 3 | 0.068055 | 1.997 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 6 | 0.003666 | 7.25 |
| w28 | 6 | 0.117806 | 8.063 |
| w29 | 3 | -0.029066 | -1.231 |
| w30 | 0 | -0.013722 | 0.0 |
| w31 | 5 | -0.005052 | -1.223 |
| w32 | 6 | 0.040561 | 3.867 |

