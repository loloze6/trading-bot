# Backtest of 050-02.b1.d3_rise-with-room-below-high_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/050-02.b1.d3_rise-with-room-below-high_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 9 | 0.074404 | 31.425 |
| w14 | 1 | -0.063967 | 0.285 |
| w15 | 6 | -0.023473 | 5.657 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | 0.053102 | 14.525 |
| w18 | 9 | -0.067278 | -0.187 |
| w19 | 15 | 0.036067 | -8.67 |
| w20 | 4 | 0.106924 | 3.668 |
| w21 | 6 | -0.096815 | -1.959 |
| w22 | 4 | -0.01256 | 10.233 |
| w23 | 6 | -0.025705 | 48.483 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.062702 | -12.146 |
| w27 | 3 | -0.089404 | -3.083 |
| w28 | 7 | 0.044109 | -0.64 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | -0.137287 | 2.456 |
| w31 | 10 | -0.008047 | -1.01 |
| w32 | 4 | 0.023055 | -2.049 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 9 | 0.171956 | 19.947 |
| w8 | 14 | -0.041834 | -12.596 |
| w9 | 6 | -0.03573 | -14.503 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | -0.018255 | -2.824 |
| w12 | 12 | 0.074219 | 7.158 |
| w13 | 8 | 0.020626 | 9.649 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.069691 | -1.608 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.04324 | 7.422 |
| w18 | 0 | None | 0.0 |
| w19 | 11 | 0.098086 | -2.415 |
| w20 | 0 | None | 0.0 |
| w21 | 10 | -0.02 | 3.493 |
| w22 | 3 | 0.005175 | 5.233 |
| w23 | 3 | -0.131465 | -7.481 |
| w24 | 7 | -0.085497 | -11.252 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | 0.028812 | -1.171 |
| w28 | 8 | -0.097894 | -15.751 |
| w29 | 0 | None | 0.0 |
| w30 | 13 | -0.028759 | -4.697 |
| w31 | 9 | -0.018817 | 7.471 |
| w32 | 7 | 0.108663 | 7.057 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 10 | 0.065465 | 1.453 |
| w11 | 4 | -0.012203 | -3.736 |
| w12 | 14 | 0.018852 | -16.606 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 9 | -0.005496 | -3.44 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.077892 | 12.454 |
| w18 | 2 | -0.028387 | 6.352 |
| w19 | 9 | 0.061338 | 7.206 |
| w20 | 7 | -0.057139 | 1.787 |
| w21 | 7 | -0.088898 | -6.77 |
| w22 | 9 | -0.012948 | 3.222 |
| w23 | 5 | -0.041221 | -12.129 |
| w24 | 9 | 0.010091 | 3.64 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.086567 | 18.264 |
| w27 | 5 | 0.173923 | 13.034 |
| w28 | 2 | 0.180561 | 4.083 |
| w29 | 5 | -0.103979 | -6.736 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 6 | 0.05889 | 4.578 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 9 | 0.139294 | -0.734 |
| w24 | 9 | -0.030913 | 7.362 |
| w25 | 6 | 0.054869 | 12.358 |
| w26 | 6 | 0.089264 | 4.502 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 5.76 |
| w30 | 7 | 0.101485 | -3.979 |
| w31 | 14 | 0.057959 | -12.827 |
| w32 | 8 | 0.030741 | 1.625 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | 0.044961 | 9.763 |
| w23 | 10 | 0.043119 | 0.95 |
| w24 | 10 | -0.123202 | -6.848 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.123684 | -13.778 |
| w27 | 11 | -0.041008 | 0.573 |
| w28 | 3 | 0.067846 | 4.459 |
| w29 | 4 | 0.060303 | 10.309 |
| w30 | 9 | -0.017912 | -16.821 |
| w31 | 7 | 0.040976 | -1.373 |
| w32 | 6 | -0.019935 | -1.402 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | -0.035683 | -2.286 |
| w21 | 10 | -0.009476 | 20.339 |
| w22 | 11 | 0.165939 | 11.969 |
| w23 | 9 | -0.030789 | -6.503 |
| w24 | 7 | -0.070573 | -3.854 |
| w25 | 5 | 0.016026 | 4.703 |
| w26 | 1 | -0.035203 | -0.437 |
| w27 | 10 | -0.033278 | 7.998 |
| w28 | 2 | -0.068404 | -4.636 |
| w29 | 6 | 0.101275 | 18.392 |
| w30 | 8 | -0.140448 | -12.496 |
| w31 | 14 | 0.080786 | -1.123 |
| w32 | 12 | -0.138671 | -2.978 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 13 | 0.04969 | -1.773 |
| w21 | 3 | -0.045033 | 3.347 |
| w22 | 10 | 0.132277 | 12.309 |
| w23 | 12 | 0.070146 | -11.875 |
| w24 | 7 | -0.058415 | -1.151 |
| w25 | 5 | 0.028126 | 12.862 |
| w26 | 16 | 0.028289 | 1.527 |
| w27 | 7 | -0.062515 | -0.514 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | 0.060539 | 14.555 |
| w30 | 17 | -0.129312 | -34.404 |
| w31 | 11 | 0.058426 | 0.678 |
| w32 | 14 | -0.033418 | -20.136 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 3 | -0.044996 | -4.178 |
| w12 | 19 | 0.000847 | -5.338 |
| w13 | 3 | 0.165919 | 14.454 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.038491 | 9.361 |
| w18 | 10 | 0.060902 | 9.573 |
| w19 | 6 | -0.127697 | -12.926 |
| w20 | 7 | 0.026871 | 6.188 |
| w21 | 5 | 0.00078 | -3.634 |
| w22 | 9 | 0.14274 | 3.759 |
| w23 | 3 | -0.169013 | -3.441 |
| w24 | 8 | 0.024649 | 0.482 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.0971 | 5.286 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | 0.123445 | 10.229 |
| w29 | 2 | -0.007473 | -1.364 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.025825 | -0.74 |
| w32 | 6 | -0.037228 | 3.4 |

