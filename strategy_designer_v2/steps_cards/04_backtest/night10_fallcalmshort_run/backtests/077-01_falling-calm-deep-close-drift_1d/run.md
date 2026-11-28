# Backtest of 077-01_falling-calm-deep-close-drift_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/077-01_falling-calm-deep-close-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 25 | 0.056128 | 11.393 |
| w13 | 4 | -0.082945 | -4.774 |
| w14 | 9 | -0.083286 | -15.432 |
| w15 | 13 | -0.005716 | -2.036 |
| w16 | 0 | None | 0.0 |
| w17 | 15 | -0.029148 | -9.226 |
| w18 | 24 | -0.084828 | -10.234 |
| w19 | 22 | 0.042001 | 8.438 |
| w21 | 0 | 0.053038 | 0.0 |
| w22 | 0 | -0.010524 | 0.0 |
| w23 | 0 | -0.027775 | 0.0 |
| w24 | 9 | 0.001642 | -2.79 |
| w25 | 18 | -0.082343 | -12.012 |
| w26 | 19 | 0.055778 | 8.637 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.070607 | -0.95 |
| w29 | 4 | 0.030803 | 1.515 |
| w30 | 35 | -0.055553 | 13.747 |
| w31 | 22 | 0.19497 | 44.53 |
| w32 | 27 | -0.090385 | -19.751 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 15 | -0.006331 | -9.898 |
| w23 | 35 | -0.101102 | -9.434 |
| w24 | 21 | 0.101059 | -13.566 |
| w25 | 2 | -0.065388 | -3.864 |
| w26 | 8 | -0.0167 | -0.558 |
| w27 | 16 | 0.054493 | -1.811 |
| w28 | 13 | -0.039035 | -3.349 |
| w29 | 19 | -0.120656 | -17.055 |
| w30 | 10 | -0.090967 | -8.045 |
| w31 | 13 | 0.074786 | 15.496 |
| w32 | 31 | -0.080569 | 0.273 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 5 | 0.10247 | 10.057 |
| w12 | 35 | -0.055367 | 11.46 |
| w13 | 5 | -0.151958 | -10.485 |
| w14 | 3 | -0.140924 | -4.135 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.084699 | -9.062 |
| w18 | 28 | -0.052632 | -9.619 |
| w19 | 12 | -0.15381 | -13.845 |
| w20 | 10 | -0.108903 | -3.801 |
| w21 | 18 | -0.041823 | -7.32 |
| w22 | 13 | -0.329211 | -22.461 |
| w23 | 12 | -0.114522 | -8.53 |
| w24 | 8 | -0.054647 | -4.214 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.10451 | -7.957 |
| w27 | 7 | -0.052309 | -10.554 |
| w28 | 6 | -0.14527 | -13.587 |
| w29 | 13 | 0.066178 | 12.239 |
| w30 | 3 | 0.010982 | -0.338 |
| w31 | 13 | -0.014104 | -2.319 |
| w32 | 5 | -0.056297 | -3.114 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 5 | -0.036168 | -2.058 |
| w26 | 12 | 0.132145 | 14.983 |
| w27 | 9 | -0.100921 | -12.578 |
| w28 | 13 | -0.046984 | -4.754 |
| w29 | 8 | -0.152577 | -10.122 |
| w30 | 13 | 0.053318 | 25.003 |
| w31 | 34 | 0.005867 | -3.083 |
| w32 | 11 | -0.030204 | -9.305 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 11 | 0.033969 | -2.234 |
| w23 | 38 | -0.018462 | 8.794 |
| w24 | 19 | 0.05935 | -14.793 |
| w25 | 0 | None | 0.0 |
| w26 | 20 | 0.060027 | 23.051 |
| w27 | 13 | -0.039782 | -11.106 |
| w28 | 15 | -0.050167 | 5.173 |
| w29 | 17 | -0.115288 | -17.29 |
| w30 | 19 | 0.011301 | 18.277 |
| w31 | 13 | 0.172249 | 32.836 |
| w32 | 19 | -0.13802 | -30.741 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 14 | 0.021079 | 11.205 |
| w21 | 20 | -0.012963 | -21.956 |
| w22 | 27 | -0.238631 | -26.539 |
| w23 | 14 | -0.048486 | -3.333 |
| w24 | 15 | 0.029031 | -5.019 |
| w25 | 6 | -0.005367 | -6.67 |
| w26 | 4 | 0.067191 | 8.743 |
| w27 | 9 | -0.070477 | -8.186 |
| w28 | 4 | 0.118885 | 10.104 |
| w29 | 11 | -0.155563 | -18.237 |
| w30 | 18 | 0.026956 | 12.591 |
| w31 | 27 | 0.064302 | 10.96 |
| w32 | 23 | -0.12134 | -13.216 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.065847 | -4.295 |
| w2 | 1 | 0.030635 | 0.602 |
| w3 | 6 | -0.101843 | -6.844 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 15 | -0.012642 | -2.351 |
| w8 | 19 | 0.005302 | 8.659 |
| w9 | 14 | 0.068653 | 32.557 |
| w10 | 4 | 0.058329 | 1.724 |
| w11 | 0 | None | 0.0 |
| w12 | 23 | -0.196881 | -28.39 |
| w13 | 4 | -0.104325 | -4.861 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.034784 | 5.477 |
| w17 | 0 | None | 0.0 |
| w18 | 11 | -0.052152 | -6.733 |
| w19 | 18 | -0.043355 | -1.287 |
| w20 | 15 | 0.067837 | 19.169 |
| w21 | 16 | 0.028264 | -13.395 |
| w22 | 5 | 0.012146 | -1.716 |
| w23 | 8 | -0.068838 | -8.543 |
| w24 | 10 | 0.055458 | -1.778 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.079649 | 1.233 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.022724 | -4.229 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.146479 | 14.741 |
| w31 | 5 | -0.020952 | -1.239 |
| w32 | 11 | -0.0535 | -2.44 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 35 | -0.252572 | -28.144 |
| w22 | 7 | -0.022393 | -3.438 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 32 | 0.001995 | 7.451 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.044797 | 1.408 |

