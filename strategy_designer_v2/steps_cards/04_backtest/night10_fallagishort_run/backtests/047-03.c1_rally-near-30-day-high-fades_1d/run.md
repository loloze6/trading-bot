# Backtest of 047-03.c1_rally-near-30-day-high-fades_1d

- Plan: `../../../../03_test_plan/night10_fallagishort_run/plans/047-03.c1_rally-near-30-day-high-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 6 | 0.066545 | 5.611 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.011161 | 0.255 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.041391 | 1.246 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | -0.103063 | -14.026 |
| w21 | 12 | -0.086515 | -0.558 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.09101 | 1.691 |
| w24 | 10 | -0.106961 | -14.99 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | -0.145186 | -20.711 |
| w27 | 0 | None | 0.0 |
| w28 | 6 | 0.043581 | 3.247 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.028163 | -7.436 |
| w31 | 6 | -0.022126 | -0.649 |
| w32 | 5 | -0.101147 | -7.394 |

- AVAXUSD: 7 of 32 windows run. 25 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days); w20, w21, w22, w23, w24, w25 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 24 | -0.05342 | -13.752 |
| w27 | 1 | 0.053125 | 0.088 |
| w28 | 32 | 0.062398 | 7.993 |
| w29 | 1 | 0.040983 | 5.707 |
| w30 | 0 | 0.014375 | 0.0 |
| w31 | 8 | 0.009119 | 3.745 |
| w32 | 5 | -0.0158 | 2.536 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | -0.025352 | -0.711 |
| w12 | 2 | 0.052745 | 1.046 |
| w13 | 8 | 0.06479 | -1.261 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.049497 | 5.165 |
| w18 | 0 | None | 0.0 |
| w19 | 7 | 0.039191 | -18.601 |
| w20 | 9 | -0.109003 | -9.003 |
| w21 | 1 | 0.012332 | -0.616 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | 0.028498 | -2.556 |
| w25 | 12 | -0.067242 | -0.843 |
| w26 | 4 | -0.008482 | -4.984 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | -0.129544 | -1.91 |
| w30 | 5 | -0.107179 | -13.159 |
| w31 | 6 | 0.034193 | 0.791 |
| w32 | 4 | 0.083323 | 0.719 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.06337 | 1.433 |
| w26 | 11 | 0.039031 | -1.607 |
| w27 | 1 | 0.119667 | 0.627 |
| w28 | 23 | 0.166201 | 6.51 |
| w29 | 0 | None | 0.0 |
| w30 | 17 | 0.026364 | 7.55 |
| w31 | 6 | 0.092262 | 5.344 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 23 | -0.009389 | -1.296 |
| w27 | 1 | 0.12984 | 2.451 |
| w28 | 14 | 0.079474 | 13.99 |
| w29 | 0 | None | 0.0 |
| w30 | 14 | 0.089168 | 8.594 |
| w31 | 8 | 0.039785 | 3.41 |
| w32 | 2 | 0.157215 | -3.525 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 16 | -0.020432 | 0.796 |
| w21 | 0 | 0.006136 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 22 | -0.070375 | -2.816 |
| w27 | 2 | 0.012317 | 0.812 |
| w28 | 28 | -0.014402 | 2.297 |
| w29 | 2 | -0.004611 | 4.205 |
| w30 | 9 | -0.040118 | 0.273 |
| w31 | 7 | 0.137309 | 4.354 |
| w32 | 0 | None | 0.0 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | -0.029101 | -22.886 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | 0.054271 | 0.0 |
| w26 | 13 | 0.024059 | 4.322 |
| w27 | 1 | 0.022859 | 0.163 |
| w28 | 17 | 0.087815 | 14.887 |
| w29 | 0 | None | 0.0 |
| w30 | 16 | -0.345492 | -10.582 |
| w31 | 22 | 0.041456 | 17.966 |
| w32 | 5 | -0.063464 | -0.925 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 6 | 0.022745 | 7.539 |
| w8 | 0 | None | 0.0 |
| w9 | 14 | 0.060932 | 10.384 |
| w10 | 5 | -0.044383 | -2.761 |
| w11 | 4 | 0.076312 | 1.956 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.038068 | 2.296 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.060639 | 0.509 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.070517 | 3.175 |
| w18 | 0 | 0.096715 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 19 | 0.001852 | -3.005 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.038717 | -0.79 |
| w24 | 5 | -0.126421 | -5.845 |
| w25 | 0 | None | 0.0 |
| w26 | 24 | 0.012708 | -1.784 |
| w27 | 0 | None | 0.0 |
| w28 | 16 | -0.017692 | -4.102 |
| w29 | 1 | 0.031273 | 4.086 |
| w30 | 16 | 0.009197 | 1.608 |
| w31 | 8 | -0.017377 | 4.71 |
| w32 | 0 | None | 0.0 |

