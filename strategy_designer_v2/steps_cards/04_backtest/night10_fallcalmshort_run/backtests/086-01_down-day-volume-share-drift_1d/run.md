# Backtest of 086-01_down-day-volume-share-drift_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/086-01_down-day-volume-share-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 33 | -0.005204 | -6.759 |
| w13 | 3 | -0.07525 | -4.247 |
| w14 | 4 | -0.032273 | -6.683 |
| w15 | 11 | -0.009671 | -10.914 |
| w16 | 0 | None | 0.0 |
| w17 | 10 | 0.012124 | 0.43 |
| w18 | 21 | -0.029499 | -5.996 |
| w19 | 24 | 0.061421 | 20.696 |
| w21 | 0 | -0.015949 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.035731 | 1.701 |
| w25 | 8 | -0.057845 | -9.648 |
| w26 | 16 | 0.060511 | 2.866 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.073874 | -1.171 |
| w29 | 1 | 0.049606 | -3.028 |
| w30 | 29 | -0.100583 | -5.388 |
| w31 | 23 | 0.143898 | 20.634 |
| w32 | 27 | -0.049699 | -2.98 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | -0.076636 | -6.935 |
| w23 | 21 | 0.010606 | 10.19 |
| w24 | 26 | 0.145076 | 11.506 |
| w25 | 0 | None | 0.0 |
| w26 | 15 | 0.107425 | -1.504 |
| w27 | 12 | 0.067295 | -5.858 |
| w28 | 10 | 0.000254 | 3.465 |
| w29 | 17 | -0.104224 | -30.616 |
| w30 | 14 | -0.050441 | -0.623 |
| w31 | 14 | 0.122282 | 29.347 |
| w32 | 29 | -0.060514 | -6.666 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 11 | 0.03428 | 3.332 |
| w12 | 37 | 0.008441 | 18.926 |
| w13 | 2 | -0.109169 | -17.485 |
| w14 | 4 | -0.118689 | -2.039 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | -0.030933 | -6.258 |
| w18 | 14 | -0.00899 | 0.533 |
| w19 | 14 | -0.270112 | -27.623 |
| w20 | 4 | -0.085141 | -1.51 |
| w21 | 14 | -0.103985 | -8.749 |
| w22 | 8 | -0.256718 | -11.576 |
| w23 | 12 | -0.136499 | -13.066 |
| w24 | 8 | -0.058566 | -3.897 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.093506 | -8.937 |
| w27 | 5 | -0.166795 | -10.362 |
| w28 | 2 | -0.05728 | -4.81 |
| w29 | 19 | 0.029476 | 5.83 |
| w30 | 2 | 0.009608 | -0.407 |
| w31 | 17 | -0.018622 | -0.578 |
| w32 | 3 | -0.0415 | -3.828 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 3 | -0.050439 | -7.65 |
| w26 | 17 | 0.132265 | 3.607 |
| w27 | 3 | -0.056028 | -7.506 |
| w28 | 12 | 0.096017 | -2.2 |
| w29 | 0 | None | 0.0 |
| w30 | 19 | -0.048935 | 1.855 |
| w31 | 37 | -0.000906 | -8.836 |
| w32 | 10 | -0.005207 | -7.286 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | 0.001663 | -1.985 |
| w23 | 26 | -0.044084 | 2.532 |
| w24 | 22 | -0.019613 | -39.129 |
| w25 | 0 | None | 0.0 |
| w26 | 17 | -0.056888 | -3.032 |
| w27 | 3 | 0.086305 | 0.501 |
| w28 | 7 | 0.100789 | 17.465 |
| w29 | 13 | -0.088508 | -18.636 |
| w30 | 18 | -0.022464 | -3.765 |
| w31 | 19 | 0.175734 | 32.411 |
| w32 | 24 | -0.201772 | -29.768 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | 0.063467 | 10.102 |
| w21 | 25 | -0.021995 | -17.794 |
| w22 | 24 | -0.207483 | -29.297 |
| w23 | 13 | -0.088449 | -2.424 |
| w24 | 17 | 0.02401 | -2.693 |
| w25 | 2 | -0.025547 | -0.226 |
| w26 | 9 | 0.030745 | 3.633 |
| w27 | 2 | 0.069817 | -0.26 |
| w28 | 7 | 0.143396 | 12.129 |
| w29 | 14 | -0.123415 | -22.884 |
| w30 | 28 | -0.062075 | 1.828 |
| w31 | 19 | 0.04176 | 5.71 |
| w32 | 32 | -0.118964 | -20.874 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.014971 | 0.884 |
| w2 | 1 | 0.030635 | 0.964 |
| w3 | 6 | -0.14515 | -15.032 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 6 | -0.002707 | -7.377 |
| w8 | 28 | -0.145256 | -9.495 |
| w9 | 11 | 0.178007 | 41.357 |
| w10 | 5 | 0.030026 | 0.827 |
| w11 | 0 | None | 0.0 |
| w12 | 41 | -0.20303 | -39.456 |
| w13 | 2 | 0.007011 | -4.415 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.034784 | -5.875 |
| w17 | 0 | None | 0.0 |
| w18 | 12 | -0.028067 | -2.578 |
| w19 | 18 | 0.012494 | -0.046 |
| w20 | 15 | 0.058272 | 33.751 |
| w21 | 28 | 0.115846 | 1.863 |
| w22 | 5 | 0.006755 | -2.868 |
| w23 | 7 | 0.000258 | -5.001 |
| w24 | 6 | 0.104666 | -1.797 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.106222 | -4.852 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | -0.022724 | -9.502 |
| w29 | 0 | None | 0.0 |
| w30 | 9 | 0.037875 | 4.911 |
| w31 | 0 | -0.000165 | 0.0 |
| w32 | 6 | -0.01844 | -4.33 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 26 | -0.122304 | -9.844 |
| w22 | 4 | -0.094322 | -4.598 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 32 | 0.071191 | 18.083 |
| w31 | 0 | None | 0.0 |
| w32 | 3 | -0.087141 | -0.033 |

