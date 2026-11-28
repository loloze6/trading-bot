# Backtest of 047-04_falling-agitated-range-scaled-fade_1d

- Plan: `../../../../03_test_plan/night10_fallagishort_run/plans/047-04_falling-agitated-range-scaled-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 16 | 0.110093 | -2.547 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | -0.000795 | -3.549 |
| w16 | 0 | None | 0.0 |
| w17 | 12 | -0.043115 | -0.948 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 33 | 0.072904 | 3.536 |
| w21 | 13 | -0.078955 | 1.407 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.099632 | -4.748 |
| w24 | 11 | -0.135833 | -16.249 |
| w25 | 0 | None | 0.0 |
| w26 | 21 | -0.049749 | -29.184 |
| w27 | 0 | None | 0.0 |
| w28 | 15 | 0.073101 | 16.01 |
| w29 | 0 | None | 0.0 |
| w30 | 6 | 0.061814 | -11.735 |
| w31 | 11 | -0.001358 | 0.355 |
| w32 | 12 | -0.050875 | -8.848 |

- AVAXUSD: 7 of 32 windows run. 25 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days); w20, w21, w22, w23, w24, w25 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 32 | -0.077101 | -28.268 |
| w27 | 1 | 0.053125 | 0.233 |
| w28 | 39 | 0.142294 | 15.564 |
| w29 | 1 | 0.040983 | 5.707 |
| w30 | 16 | -0.024293 | 2.212 |
| w31 | 9 | -0.012656 | 12.287 |
| w32 | 5 | -0.013926 | -6.526 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 5 | -0.013778 | -4.085 |
| w12 | 1 | 0.089271 | 0.911 |
| w13 | 21 | 0.061057 | -8.759 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 18 | 0.027901 | 7.303 |
| w18 | 0 | None | 0.0 |
| w19 | 11 | -0.008434 | -28.935 |
| w20 | 27 | -0.102363 | -21.096 |
| w21 | 4 | 0.001555 | -3.831 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.086509 | -8.569 |
| w25 | 24 | -0.06805 | -14.123 |
| w26 | 4 | 0.028735 | -6.77 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | -0.175698 | -11.845 |
| w30 | 8 | -0.051974 | -8.256 |
| w31 | 16 | -0.049302 | -1.073 |
| w32 | 9 | 0.082441 | 2.291 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 9 | 0.026355 | 0.074 |
| w26 | 19 | 0.0743 | -11.371 |
| w27 | 2 | 0.120526 | 4.225 |
| w28 | 31 | 0.141058 | 13.341 |
| w29 | 0 | None | 0.0 |
| w30 | 24 | 0.030396 | 32.146 |
| w31 | 8 | 0.039105 | 14.674 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 30 | -0.086699 | -17.333 |
| w27 | 1 | 0.12984 | 6.229 |
| w28 | 23 | 0.058903 | 21.935 |
| w29 | 0 | None | 0.0 |
| w30 | 22 | 0.045767 | 4.856 |
| w31 | 12 | 0.06046 | 14.203 |
| w32 | 2 | 0.157215 | -3.525 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 26 | 0.040426 | -10.561 |
| w21 | 2 | 0.006136 | -5.542 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 33 | -0.061796 | -12.44 |
| w27 | 2 | 0.012317 | 1.217 |
| w28 | 32 | 0.017339 | 8.19 |
| w29 | 2 | -0.004611 | 4.205 |
| w30 | 11 | -0.042827 | 0.83 |
| w31 | 10 | 0.023992 | 5.808 |
| w32 | 0 | None | 0.0 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | -0.024186 | -23.362 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 5 | 0.023677 | 1.941 |
| w26 | 25 | 0.011581 | -5.135 |
| w27 | 1 | 0.022859 | 0.343 |
| w28 | 24 | 0.076848 | 6.654 |
| w29 | 0 | None | 0.0 |
| w30 | 23 | -0.392383 | -39.493 |
| w31 | 28 | -0.052116 | 19.122 |
| w32 | 15 | -0.07593 | -4.796 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | -0.0133 | -11.44 |
| w8 | 0 | None | 0.0 |
| w9 | 19 | -0.019981 | 6.927 |
| w10 | 8 | -0.003319 | 0.787 |
| w11 | 7 | 0.073045 | 15.467 |
| w12 | 0 | None | 0.0 |
| w13 | 17 | 0.112812 | 7.374 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | 0.013286 | 1.16 |
| w16 | 0 | None | 0.0 |
| w17 | 20 | -0.006057 | 1.619 |
| w18 | 3 | 0.020474 | 1.955 |
| w19 | 0 | None | 0.0 |
| w20 | 24 | 0.1865 | 10.978 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 13 | -0.00754 | 4.723 |
| w24 | 2 | -0.17265 | -13.735 |
| w25 | 0 | None | 0.0 |
| w26 | 29 | 0.013273 | -18.829 |
| w27 | 0 | None | 0.0 |
| w28 | 24 | 0.021312 | -10.301 |
| w29 | 1 | 0.031273 | 4.086 |
| w30 | 23 | 0.020181 | 0.367 |
| w31 | 12 | -0.019836 | 11.094 |
| w32 | 0 | None | 0.0 |

