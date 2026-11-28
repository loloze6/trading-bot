# Backtest of 089-04_calm-decline-up-volume-lasting_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/089-04_calm-decline-up-volume-lasting_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 6 | -0.009313 | 29.86 |
| w14 | 5 | -0.035604 | -0.463 |
| w15 | 9 | 0.026656 | 10.083 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.027127 | 15.329 |
| w18 | 6 | 0.132116 | -1.159 |
| w19 | 9 | -0.149541 | -5.032 |
| w20 | 5 | 0.010813 | -21.955 |
| w21 | 7 | -0.102546 | -9.088 |
| w22 | 7 | 0.067028 | 1.286 |
| w23 | 5 | 0.004782 | -11.689 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | 0.004667 | -1.812 |
| w27 | 6 | 0.015942 | -3.302 |
| w28 | 9 | -0.038632 | -6.464 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | -0.128842 | -0.441 |
| w31 | 10 | -0.034004 | -5.438 |
| w32 | 6 | -0.088958 | -19.171 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | 0.082303 | 15.11 |
| w8 | 11 | 0.166933 | 4.528 |
| w9 | 8 | 0.066891 | -2.123 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | -0.027269 | 0.0 |
| w12 | 3 | -0.023778 | -5.735 |
| w13 | 5 | 0.001808 | 21.409 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.049694 | 7.869 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.020562 | -0.183 |
| w19 | 5 | 0.168467 | 9.297 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.007082 | 9.916 |
| w23 | 0 | None | 0.0 |
| w24 | 9 | 0.081929 | -5.345 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | -0.099957 | -7.684 |
| w28 | 8 | 0.048803 | -22.518 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | -0.124052 | -5.696 |
| w31 | 8 | -0.024721 | 4.305 |
| w32 | 7 | 0.008309 | 0.842 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 12 | -0.039569 | -3.192 |
| w11 | 2 | -0.127122 | -2.413 |
| w12 | 9 | -0.215089 | -36.295 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.081071 | 0.232 |
| w15 | 7 | -0.019527 | -5.874 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.094477 | 13.83 |
| w18 | 0 | None | 0.0 |
| w19 | 19 | -0.074185 | -6.529 |
| w20 | 4 | -0.05761 | 1.782 |
| w21 | 9 | -0.032882 | -34.967 |
| w22 | 12 | 0.001084 | 3.924 |
| w23 | 11 | 0.013209 | -15.432 |
| w24 | 16 | 0.028372 | 3.501 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | -0.103836 | -6.637 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | 0.180561 | 1.761 |
| w29 | 4 | -0.105583 | -3.465 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | 0.041338 | -4.451 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 11 | -0.031579 | 0.33 |
| w24 | 4 | 0.114911 | 25.367 |
| w25 | 3 | 0.059107 | 35.422 |
| w26 | 5 | 0.034592 | -5.274 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 15.226 |
| w30 | 7 | -0.123867 | -14.807 |
| w31 | 9 | 0.074119 | -15.818 |
| w32 | 2 | 0.021058 | 5.832 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 7 | 0.017302 | 20.892 |
| w23 | 18 | 0.129517 | -12.456 |
| w24 | 4 | -0.144794 | -7.328 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.057538 | -17.331 |
| w27 | 10 | 0.044775 | -2.502 |
| w28 | 12 | 0.073537 | 2.362 |
| w29 | 6 | -0.000158 | 11.579 |
| w30 | 3 | -0.009587 | -3.688 |
| w31 | 9 | 0.00776 | -11.109 |
| w32 | 3 | -0.034343 | -5.95 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 8 | 0.029183 | -0.794 |
| w21 | 3 | 0.035657 | 0.061 |
| w22 | 12 | 0.144399 | 14.15 |
| w23 | 8 | -0.126488 | -24.141 |
| w24 | 8 | -0.097492 | -13.139 |
| w25 | 4 | 0.00065 | 36.761 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | 0.005176 | 2.358 |
| w28 | 0 | -0.035978 | 0.0 |
| w29 | 4 | -0.015293 | 29.406 |
| w30 | 1 | -0.035641 | -1.421 |
| w31 | 10 | -0.040163 | -3.954 |
| w32 | 10 | -0.033318 | 10.477 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 15 | 0.034756 | -28.106 |
| w21 | 2 | -0.006762 | -0.905 |
| w22 | 7 | 0.059424 | -5.573 |
| w23 | 11 | -0.065547 | -4.518 |
| w24 | 10 | -0.021733 | 4.635 |
| w25 | 6 | 0.04632 | 26.668 |
| w26 | 5 | 0.002978 | -4.302 |
| w27 | 8 | 0.022991 | 9.072 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.448973 | 28.111 |
| w30 | 8 | -0.115201 | -11.66 |
| w31 | 19 | -0.040356 | -3.885 |
| w32 | 17 | -0.05502 | -11.659 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 1 | -0.020376 | -2.487 |
| w12 | 8 | -0.042967 | 5.177 |
| w13 | 4 | 0.078447 | 1.176 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.017318 | 6.153 |
| w18 | 11 | 0.059049 | 2.111 |
| w19 | 4 | -0.11576 | -9.451 |
| w20 | 11 | 0.034443 | 7.045 |
| w21 | 4 | 0.02987 | 1.445 |
| w22 | 9 | 0.051456 | 1.491 |
| w23 | 2 | -0.169013 | -0.907 |
| w24 | 3 | 0.068055 | 4.725 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 6 | 0.003666 | 1.798 |
| w28 | 6 | 0.117806 | 22.966 |
| w29 | 2 | -0.029066 | -3.804 |
| w30 | 0 | -0.013722 | 0.0 |
| w31 | 3 | -0.005052 | -1.13 |
| w32 | 6 | 0.040561 | 5.368 |

