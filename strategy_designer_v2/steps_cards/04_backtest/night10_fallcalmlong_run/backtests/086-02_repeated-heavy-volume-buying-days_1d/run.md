# Backtest of 086-02_repeated-heavy-volume-buying-days_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/086-02_repeated-heavy-volume-buying-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 5 | 0.027839 | 9.336 |
| w14 | 2 | 0.043243 | -1.543 |
| w15 | 2 | -0.022537 | -1.891 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.032547 | 8.048 |
| w18 | 1 | -0.130101 | -3.966 |
| w19 | 11 | -0.055996 | -6.644 |
| w20 | 1 | -0.032965 | 2.133 |
| w21 | 3 | -0.096422 | -6.895 |
| w22 | 2 | -0.022718 | 3.705 |
| w23 | 7 | -0.022536 | -0.794 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | -0.081926 | -11.646 |
| w27 | 5 | -0.007871 | -5.672 |
| w28 | 7 | 0.29146 | 24.598 |
| w29 | 0 | None | 0.0 |
| w30 | 2 | 0.007135 | -0.894 |
| w31 | 6 | -0.063882 | -4.424 |
| w32 | 2 | -0.092712 | -2.421 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 9 | 0.053348 | 1.703 |
| w8 | 4 | -0.125932 | -18.248 |
| w9 | 1 | -0.025685 | -0.557 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.046415 | -2.03 |
| w12 | 14 | 0.036465 | 7.586 |
| w13 | 5 | -0.028468 | 10.909 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.029657 | 12.954 |
| w18 | 0 | None | 0.0 |
| w19 | 14 | -0.022296 | -2.18 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.027274 | -0.738 |
| w22 | 2 | -0.02916 | 8.208 |
| w23 | 6 | -0.092348 | 9.778 |
| w24 | 4 | 0.066262 | 0.257 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | -0.22568 | -13.497 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | -0.07537 | -10.704 |
| w31 | 6 | -0.076527 | -5.706 |
| w32 | 9 | -0.113022 | -1.033 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 4 | -0.056518 | -2.039 |
| w11 | 0 | -0.105008 | 0.0 |
| w12 | 18 | 0.033869 | -0.924 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.063011 | -13.898 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.002444 | 6.711 |
| w18 | 0 | None | 0.0 |
| w19 | 11 | 0.046174 | 1.641 |
| w20 | 11 | 0.087495 | -3.336 |
| w21 | 12 | -0.031302 | -10.9 |
| w22 | 13 | -0.068661 | 12.132 |
| w23 | 5 | 0.11718 | -8.523 |
| w24 | 15 | 0.087274 | -3.483 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.010519 | 3.904 |
| w27 | 2 | -0.002343 | 13.259 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | -0.02651 | 8.317 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.038471 | 3.805 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 1 | 0.159157 | 15.732 |
| w24 | 3 | 0.159116 | 28.963 |
| w25 | 7 | 0.081589 | 19.023 |
| w26 | 4 | 0.105209 | 9.531 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | -0.100024 | -16.951 |
| w31 | 9 | 0.10352 | -4.547 |
| w32 | 5 | -0.006459 | 7.825 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | -0.047292 | 4.322 |
| w23 | 14 | -0.029551 | -27.57 |
| w24 | 7 | -0.014199 | 0.459 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | -0.116175 | -15.717 |
| w27 | 7 | 0.028458 | -0.794 |
| w28 | 4 | -0.045595 | -1.414 |
| w29 | 2 | -0.010234 | 1.636 |
| w30 | 3 | -0.04926 | -14.164 |
| w31 | 0 | None | 0.0 |
| w32 | 10 | -0.07837 | -9.753 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 3 | -0.006094 | -10.903 |
| w21 | 2 | 0.005434 | 14.256 |
| w22 | 12 | 0.181118 | 9.593 |
| w23 | 7 | 0.009269 | -27.951 |
| w24 | 2 | -0.064992 | -5.537 |
| w25 | 2 | -0.009642 | 5.753 |
| w26 | 0 | 0.077434 | 0.0 |
| w27 | 5 | -0.029929 | 3.182 |
| w28 | 0 | -0.042739 | 0.0 |
| w29 | 4 | 0.100952 | 15.978 |
| w30 | 7 | 0.026209 | -18.997 |
| w31 | 12 | 0.200059 | 4.476 |
| w32 | 12 | 0.056263 | 13.518 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | 0.06435 | 8.897 |
| w21 | 0 | None | 0.0 |
| w22 | 9 | -0.004463 | -18.56 |
| w23 | 12 | -0.02207 | -3.11 |
| w24 | 5 | -0.066841 | -5.487 |
| w25 | 4 | 0.004832 | 7.656 |
| w26 | 6 | -0.100689 | 0.857 |
| w27 | 5 | 0.021467 | 10.616 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.16683 | 41.468 |
| w30 | 17 | 0.010407 | -26.596 |
| w31 | 10 | -0.00527 | 4.251 |
| w32 | 5 | 0.010159 | -6.289 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | 0.130255 | 0.136 |
| w12 | 12 | -0.057085 | 2.777 |
| w13 | 1 | 0.119068 | 18.518 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.069962 | 15.68 |
| w18 | 7 | 0.012552 | 5.23 |
| w19 | 7 | -0.075125 | -11.923 |
| w20 | 3 | -0.020486 | 0.261 |
| w21 | 2 | 0.050916 | -0.371 |
| w22 | 4 | 0.044232 | 2.606 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 1 | 0.094179 | 5.0 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.033079 | -9.487 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | -0.011162 | -4.619 |
| w32 | 2 | 0.02345 | 0.503 |

