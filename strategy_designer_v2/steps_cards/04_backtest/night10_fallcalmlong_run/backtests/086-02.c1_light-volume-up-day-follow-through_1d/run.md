# Backtest of 086-02.c1_light-volume-up-day-follow-through_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/086-02.c1_light-volume-up-day-follow-through_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 6 | 0.034182 | 4.049 |
| w14 | 6 | -0.059631 | 3.375 |
| w15 | 5 | -0.003749 | 8.997 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | -0.023466 | 4.547 |
| w18 | 10 | 0.063254 | 5.218 |
| w19 | 25 | 0.058049 | -6.744 |
| w20 | 3 | 0.052913 | 4.145 |
| w21 | 12 | -0.011817 | -2.114 |
| w22 | 8 | 0.051271 | 0.235 |
| w23 | 6 | -0.033574 | -4.525 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 11 | -0.053484 | -16.265 |
| w27 | 7 | 0.114896 | 2.158 |
| w28 | 10 | -0.009896 | -14.546 |
| w29 | 0 | None | 0.0 |
| w30 | 10 | 0.092042 | 2.133 |
| w31 | 17 | 0.010075 | -4.62 |
| w32 | 15 | -0.034765 | -22.361 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 13 | 0.121366 | 13.908 |
| w8 | 18 | 0.05993 | -6.2 |
| w9 | 7 | -0.036091 | -6.583 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | 0.099586 | -0.926 |
| w12 | 22 | 0.063323 | -0.475 |
| w13 | 4 | -0.027046 | 10.686 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | -0.003968 | 17.049 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.018846 | 6.361 |
| w18 | 1 | -0.020562 | -0.12 |
| w19 | 18 | 0.066869 | 2.724 |
| w20 | 0 | None | 0.0 |
| w21 | 11 | 0.022794 | 8.711 |
| w22 | 3 | 0.042447 | 2.46 |
| w23 | 4 | 0.011362 | 8.165 |
| w24 | 10 | 0.058405 | 1.881 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.050646 | 3.518 |
| w28 | 4 | -0.025507 | -8.738 |
| w29 | 0 | None | 0.0 |
| w30 | 17 | 0.013961 | -0.967 |
| w31 | 10 | 0.128704 | 11.977 |
| w32 | 8 | 0.090175 | -1.377 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 8 | -0.080097 | -2.841 |
| w11 | 4 | 0.073244 | -1.007 |
| w12 | 14 | 0.08324 | -6.592 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | -0.059349 | -0.412 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | 0.071389 | 8.331 |
| w18 | 5 | 0.119271 | 11.659 |
| w19 | 15 | 0.004407 | 24.571 |
| w20 | 5 | 0.171244 | 17.466 |
| w21 | 12 | -0.014119 | -8.0 |
| w22 | 8 | -0.138317 | 0.523 |
| w23 | 13 | 0.129755 | -13.639 |
| w24 | 12 | 0.042907 | 4.314 |
| w25 | 0 | None | 0.0 |
| w26 | 10 | -0.012469 | 5.323 |
| w27 | 5 | 0.131441 | 9.32 |
| w28 | 0 | None | 0.0 |
| w29 | 12 | -0.025889 | 3.997 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | 0.026395 | 2.751 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 11 | 0.006178 | 0.24 |
| w24 | 7 | -0.021371 | 7.677 |
| w25 | 4 | 0.029652 | 2.242 |
| w26 | 4 | -0.077317 | -6.15 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | -0.241607 | -5.311 |
| w29 | 0 | None | 0.0 |
| w30 | 9 | 0.002874 | -8.562 |
| w31 | 19 | 0.077099 | 16.644 |
| w32 | 7 | -0.099224 | -4.329 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | 0.021391 | 8.872 |
| w23 | 23 | 0.154419 | -2.939 |
| w24 | 15 | -0.079563 | -4.191 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.162155 | -18.77 |
| w27 | 6 | 0.014565 | 8.078 |
| w28 | 12 | 0.140969 | -3.617 |
| w29 | 9 | 0.055623 | 3.618 |
| w30 | 7 | -0.044466 | -10.79 |
| w31 | 15 | -0.026668 | -15.45 |
| w32 | 12 | -0.114299 | 6.351 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 6 | 0.046719 | 6.459 |
| w21 | 13 | 0.044019 | 6.909 |
| w22 | 9 | 0.016445 | 19.356 |
| w23 | 12 | 0.018582 | -0.093 |
| w24 | 15 | -0.062863 | -6.04 |
| w25 | 5 | 0.009374 | 12.858 |
| w26 | 3 | -0.10596 | -8.517 |
| w27 | 4 | 0.10743 | 7.441 |
| w28 | 1 | -0.009876 | -10.197 |
| w29 | 8 | 0.184735 | 22.976 |
| w30 | 8 | -0.056527 | -20.343 |
| w31 | 19 | 0.019898 | -1.308 |
| w32 | 13 | 0.005249 | 21.27 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | -0.00135 | 3.543 |
| w21 | 4 | -0.042862 | 6.512 |
| w22 | 14 | 0.232652 | 16.653 |
| w23 | 16 | -0.11144 | -21.284 |
| w24 | 16 | -0.063659 | -2.351 |
| w25 | 8 | 0.120412 | 9.967 |
| w26 | 18 | 0.073422 | -21.753 |
| w27 | 3 | -0.091859 | -0.3 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | 0.150247 | 40.784 |
| w30 | 24 | 0.078693 | -21.621 |
| w31 | 14 | 0.11423 | 8.667 |
| w32 | 21 | 0.029418 | 11.732 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 4 | -0.018877 | -3.324 |
| w12 | 25 | -0.013968 | -4.569 |
| w13 | 5 | 0.00267 | 6.886 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.043524 | 4.228 |
| w18 | 11 | 0.218196 | 7.794 |
| w19 | 7 | -0.038933 | 11.271 |
| w20 | 5 | -0.054453 | 2.277 |
| w21 | 3 | 0.018668 | 0.293 |
| w22 | 6 | 0.072606 | 0.942 |
| w23 | 7 | 0.115516 | 5.418 |
| w24 | 6 | -0.019079 | 3.768 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.020172 | 15.765 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | -0.035845 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 9 | -0.031453 | 1.344 |
| w32 | 5 | 0.022431 | 5.077 |

