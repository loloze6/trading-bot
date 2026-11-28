# Backtest of 086-01.c1_heavy-volume-off-low-absorption_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/086-01.c1_heavy-volume-off-low-absorption_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 5 | -0.034669 | 15.321 |
| w14 | 2 | 0.024652 | 0.038 |
| w15 | 3 | 0.033515 | -1.651 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.002272 | -2.563 |
| w18 | 4 | -0.062382 | -0.593 |
| w19 | 13 | 0.02749 | 24.868 |
| w20 | 4 | -0.036122 | -9.155 |
| w21 | 9 | -0.064886 | -8.582 |
| w22 | 4 | 0.036034 | 1.939 |
| w23 | 9 | -0.013176 | -4.185 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | 0.068816 | -0.1 |
| w27 | 3 | -0.102781 | -5.368 |
| w28 | 7 | 0.114465 | 42.057 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.149384 | 0.313 |
| w31 | 4 | 0.042887 | -6.249 |
| w32 | 11 | -0.184619 | -61.723 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 11 | -0.035232 | -15.313 |
| w8 | 10 | -0.071139 | -18.162 |
| w9 | 3 | -0.042582 | -24.968 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | -0.036242 | 3.563 |
| w12 | 10 | 0.042766 | 8.604 |
| w13 | 3 | -0.040624 | -1.539 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.047612 | 11.286 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.014822 | 7.312 |
| w18 | 0 | None | 0.0 |
| w19 | 10 | 0.138824 | 22.118 |
| w20 | 0 | 0.088467 | 0.0 |
| w21 | 5 | -0.044822 | -0.841 |
| w22 | 2 | -0.040822 | 9.205 |
| w23 | 3 | 0.058473 | 1.803 |
| w24 | 8 | -0.030203 | 5.778 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | -0.103766 | 0.0 |
| w28 | 1 | -0.22568 | -3.88 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.026601 | -10.139 |
| w31 | 2 | -0.028343 | -9.513 |
| w32 | 4 | -0.187024 | -6.466 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 8 | 0.007374 | 8.479 |
| w11 | 3 | -0.110364 | -12.643 |
| w12 | 16 | -0.012238 | 3.93 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.015277 | -6.304 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.00402 | 1.746 |
| w18 | 0 | None | 0.0 |
| w19 | 13 | 0.216091 | 13.48 |
| w20 | 7 | 0.003858 | -1.4 |
| w21 | 13 | -0.07153 | -13.208 |
| w22 | 13 | 0.005021 | 23.485 |
| w23 | 5 | 0.086774 | 13.114 |
| w24 | 6 | 0.049449 | 5.44 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.076761 | 2.012 |
| w27 | 2 | -0.079549 | 1.319 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.131428 | 0.342 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | -0.040727 | -0.932 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 14 | -0.042907 | -18.573 |
| w24 | 4 | 0.027167 | 10.519 |
| w25 | 7 | 0.040691 | 8.409 |
| w26 | 5 | 0.014435 | 4.04 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.079391 | 7.963 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | 0.046645 | -6.712 |
| w31 | 12 | 0.014937 | -30.501 |
| w32 | 12 | -0.105717 | 0.298 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | -0.09045 | 5.213 |
| w23 | 20 | -0.004132 | -30.537 |
| w24 | 8 | -0.087578 | -7.026 |
| w25 | 0 | None | 0.0 |
| w26 | 11 | -0.01926 | -18.425 |
| w27 | 12 | 0.074935 | 9.239 |
| w28 | 6 | -0.063724 | -3.709 |
| w29 | 5 | 0.089313 | 7.117 |
| w30 | 4 | -0.011496 | -1.177 |
| w31 | 5 | -0.133048 | -17.76 |
| w32 | 10 | 0.138568 | 8.968 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 5 | 0.03647 | 3.615 |
| w21 | 5 | -0.013877 | 47.626 |
| w22 | 9 | 0.020586 | 10.184 |
| w23 | 7 | -0.093689 | -18.26 |
| w24 | 3 | -0.018329 | 0.705 |
| w25 | 2 | -0.009642 | 5.753 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.179523 | 13.565 |
| w30 | 6 | 0.038716 | -0.235 |
| w31 | 12 | -0.028224 | -10.082 |
| w32 | 11 | 0.138119 | 36.414 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | 0.229016 | 13.563 |
| w21 | 3 | -0.002181 | -0.533 |
| w22 | 11 | -0.064336 | -15.892 |
| w23 | 18 | -0.030108 | -22.054 |
| w24 | 6 | -0.0594 | -11.548 |
| w25 | 4 | -0.02666 | 8.231 |
| w26 | 14 | 0.155033 | 12.973 |
| w27 | 3 | 0.029176 | 11.612 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.057532 | 2.566 |
| w30 | 24 | 0.012937 | -15.097 |
| w31 | 12 | -0.011054 | 16.947 |
| w32 | 8 | -0.030384 | -15.817 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | -0.011406 | 2.77 |
| w12 | 13 | 0.117382 | 3.255 |
| w13 | 2 | -0.016986 | 18.482 |
| w14 | 2 | -0.04099 | 1.15 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.053584 | 3.336 |
| w18 | 4 | 0.118735 | 5.597 |
| w19 | 4 | 0.043536 | 6.44 |
| w20 | 4 | 0.082801 | -2.145 |
| w21 | 5 | -0.12497 | -4.8 |
| w22 | 5 | 0.19744 | 12.864 |
| w23 | 5 | 0.047463 | 0.453 |
| w24 | 0 | 0.072263 | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.036248 | 2.452 |
| w27 | 3 | -0.100588 | 4.832 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | -0.031091 | -6.998 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.055025 | -8.206 |
| w32 | 0 | None | 0.0 |

