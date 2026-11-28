# Backtest of 050-03.c1_calm-downtrend-3-day-fall-continues_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/050-03.c1_calm-downtrend-3-day-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 35 | 0.097786 | 23.197 |
| w13 | 4 | -0.01641 | -0.768 |
| w14 | 9 | -0.010048 | -1.908 |
| w15 | 11 | -0.002717 | -0.674 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | -0.022173 | -4.596 |
| w18 | 17 | -0.019169 | -0.519 |
| w19 | 26 | 0.134551 | 24.725 |
| w21 | 0 | 0.041747 | 0.0 |
| w22 | 0 | -0.052014 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.075021 | 7.7 |
| w25 | 14 | -0.037703 | -10.666 |
| w26 | 20 | 0.034802 | 9.966 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.010109 | 0.041 |
| w30 | 42 | -0.006259 | 17.355 |
| w31 | 26 | 0.171702 | 26.335 |
| w32 | 40 | -0.041024 | -8.683 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | 0.088216 | 3.696 |
| w23 | 38 | -0.086611 | -17.24 |
| w24 | 30 | 0.09305 | -10.062 |
| w25 | 2 | -0.04509 | -5.108 |
| w26 | 8 | 0.128998 | 8.891 |
| w27 | 15 | 0.086317 | 4.011 |
| w28 | 12 | -0.040955 | -0.226 |
| w29 | 16 | -0.124034 | -20.505 |
| w30 | 15 | -0.036707 | -2.591 |
| w31 | 17 | -0.034147 | -0.119 |
| w32 | 46 | 0.045126 | 11.869 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 8 | 0.081274 | 2.604 |
| w12 | 46 | -0.02627 | 8.476 |
| w13 | 4 | -0.091931 | -5.769 |
| w14 | 4 | -0.144974 | -3.466 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | -0.056708 | -8.202 |
| w18 | 19 | -0.05052 | -8.957 |
| w19 | 9 | 0.093905 | 2.482 |
| w20 | 8 | -0.10618 | -4.57 |
| w21 | 17 | 0.000802 | -2.294 |
| w22 | 12 | -0.265611 | -23.816 |
| w23 | 13 | -0.08715 | -12.254 |
| w24 | 11 | -0.087356 | -8.694 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | -0.171288 | -10.25 |
| w27 | 3 | -0.012664 | -4.826 |
| w28 | 4 | -0.057225 | -5.523 |
| w29 | 13 | 0.048099 | 10.722 |
| w30 | 2 | 0.002382 | 0.129 |
| w31 | 14 | -0.028923 | -5.141 |
| w32 | 2 | -0.074777 | -4.469 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 2 | -0.00206 | 0.252 |
| w26 | 14 | 0.162415 | 15.739 |
| w27 | 8 | -0.085853 | -13.539 |
| w28 | 18 | -0.114441 | -8.084 |
| w29 | 3 | -0.013012 | -2.885 |
| w30 | 21 | 0.118729 | 22.315 |
| w31 | 39 | -0.052336 | -3.234 |
| w32 | 8 | 0.008834 | -2.473 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | 0.072079 | 3.424 |
| w23 | 40 | 0.041578 | 11.022 |
| w24 | 21 | 0.051501 | -15.707 |
| w25 | 0 | None | 0.0 |
| w26 | 21 | -0.053972 | 0.497 |
| w27 | 10 | -0.007987 | -5.953 |
| w28 | 14 | -0.102057 | -7.526 |
| w29 | 17 | -0.08774 | -14.215 |
| w30 | 21 | 0.04218 | 18.156 |
| w31 | 17 | 0.079515 | 12.421 |
| w32 | 30 | -0.176354 | -39.089 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 14 | 0.013693 | 2.581 |
| w21 | 23 | 0.004901 | -10.214 |
| w22 | 17 | -0.142003 | -20.304 |
| w23 | 19 | -0.051962 | -8.357 |
| w24 | 19 | 0.03443 | -4.681 |
| w25 | 4 | -0.026056 | -4.753 |
| w26 | 9 | 0.046723 | -1.256 |
| w27 | 5 | -0.048589 | -5.917 |
| w28 | 9 | 0.079559 | 6.768 |
| w29 | 8 | -0.095186 | -8.361 |
| w30 | 29 | -0.061805 | -4.078 |
| w31 | 29 | -0.024536 | -0.825 |
| w32 | 39 | -0.127742 | -14.664 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | -0.097122 | -4.705 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | 0.063003 | 5.189 |
| w8 | 24 | -0.06922 | -2.605 |
| w9 | 12 | 0.022333 | 11.987 |
| w10 | 7 | 0.033185 | 0.172 |
| w11 | 0 | None | 0.0 |
| w12 | 41 | -0.297865 | -46.101 |
| w13 | 4 | -0.031463 | -3.203 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.034784 | 4.877 |
| w17 | 0 | None | 0.0 |
| w18 | 10 | -0.049411 | -5.452 |
| w19 | 20 | 0.039742 | 3.453 |
| w20 | 8 | 0.149915 | 36.436 |
| w21 | 22 | 0.145402 | -5.186 |
| w22 | 0 | 0.006236 | 0.0 |
| w23 | 8 | -0.035026 | -14.983 |
| w24 | 13 | 0.034286 | -3.472 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.04871 | 3.072 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.022724 | -4.229 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | 0.223899 | 10.298 |
| w31 | 4 | 0.007272 | 0.112 |
| w32 | 15 | -0.193455 | -6.018 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 32 | -0.211024 | -26.971 |
| w22 | 3 | -0.020694 | -3.105 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 30 | 0.0167 | 5.94 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

