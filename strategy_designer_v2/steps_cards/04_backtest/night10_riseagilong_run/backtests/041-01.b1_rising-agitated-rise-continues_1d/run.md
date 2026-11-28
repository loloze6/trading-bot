# Backtest of 041-01.b1_rising-agitated-rise-continues_1d

- Plan: `../../../../03_test_plan/night10_riseagilong_run/plans/041-01.b1_rising-agitated-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | -0.131981 | 0.0 |
| w3 | 3 | -0.088801 | -3.579 |
| w4 | 21 | -0.084671 | -5.614 |
| w5 | 47 | 0.025709 | 19.481 |
| w6 | 23 | 0.102787 | 22.873 |
| w7 | 11 | -0.214563 | -12.809 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 26 | -0.077532 | -3.579 |
| w11 | 18 | 0.040332 | 2.942 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.027477 | -1.826 |
| w14 | 11 | 0.012768 | 2.315 |
| w15 | 32 | 0.067833 | 15.347 |
| w16 | 47 | 0.019417 | 10.863 |
| w17 | 8 | -0.147804 | -15.434 |
| w18 | 11 | -0.047406 | -4.014 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | 0.109302 | 7.445 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | -0.133904 | -7.194 |
| w24 | 0 | None | 0.0 |
| w25 | 25 | -0.220714 | -19.846 |
| w26 | 0 | None | 0.0 |
| w27 | 30 | -0.085684 | -8.714 |
| w28 | 24 | 0.100823 | 5.977 |
| w29 | 5 | -0.082239 | -2.821 |
| w30 | 1 | 0.029313 | 0.487 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 26 | -0.020267 | -1.762 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | -0.032204 | -0.583 |
| w11 | 14 | -0.08103 | -6.691 |
| w12 | 0 | None | 0.0 |
| w13 | 10 | -0.095918 | -10.754 |
| w14 | 14 | -0.098057 | -4.261 |
| w15 | 28 | -0.049666 | -1.103 |
| w16 | 44 | 0.081752 | 48.441 |
| w17 | 19 | -0.219604 | -26.097 |
| w18 | 12 | 0.087882 | 5.596 |
| w19 | 0 | None | 0.0 |
| w20 | 10 | -0.025102 | -3.546 |
| w21 | 6 | -0.13708 | -5.878 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 22 | -0.12868 | -10.582 |
| w25 | 28 | -0.121567 | -12.538 |
| w26 | 8 | -0.041225 | -3.366 |
| w27 | 24 | -0.001847 | 5.225 |
| w28 | 5 | 0.015139 | -0.827 |
| w29 | 13 | -0.082975 | -3.5 |
| w30 | 5 | 0.029482 | 0.371 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.108914 | -5.133 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 13 | -0.169894 | -17.118 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | -0.133817 | -13.624 |
| w14 | 6 | -0.170287 | -8.655 |
| w15 | 31 | -0.165178 | -15.811 |
| w16 | 34 | -0.071833 | 1.514 |
| w17 | 16 | -0.142947 | -10.409 |
| w18 | 8 | -0.016757 | -2.012 |
| w19 | 7 | 0.02278 | 0.305 |
| w20 | 3 | -0.332303 | -22.719 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.068962 | 4.246 |
| w25 | 1 | -0.003777 | -0.46 |
| w26 | 26 | -0.052803 | -5.166 |
| w27 | 16 | -0.316813 | -28.862 |
| w28 | 30 | 0.048395 | 10.607 |
| w29 | 15 | -0.049947 | -7.968 |
| w30 | 32 | -0.012384 | 3.509 |
| w31 | 8 | 0.006012 | 0.487 |
| w32 | 4 | -0.256042 | -17.513 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 15 | -0.151497 | -16.113 |
| w26 | 1 | -0.125573 | -6.38 |
| w27 | 14 | 0.017394 | 0.885 |
| w28 | 5 | 0.136165 | 5.799 |
| w29 | 10 | 0.020047 | 1.036 |
| w30 | 5 | 0.04845 | 0.055 |
| w31 | 0 | None | 0.0 |
| w32 | 11 | -0.113366 | -8.501 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 21 | -0.207222 | -17.697 |
| w25 | 25 | -0.174949 | -20.673 |
| w26 | 1 | -0.130783 | -5.757 |
| w27 | 21 | 0.024348 | 3.059 |
| w28 | 4 | 0.146435 | 5.035 |
| w29 | 8 | -0.083443 | -6.63 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 17 | -0.107896 | -8.034 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 22 | -0.101447 | -6.507 |
| w25 | 31 | -0.065226 | -7.193 |
| w26 | 1 | -0.049294 | -0.71 |
| w27 | 29 | 0.392934 | 112.259 |
| w28 | 6 | 0.065881 | 1.223 |
| w29 | 20 | -0.139721 | -12.421 |
| w30 | 1 | 0.061419 | 0.467 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 2 | -0.080921 | -3.754 |
| w13 | 10 | -0.045924 | -4.204 |
| w14 | 8 | -0.073057 | -3.844 |
| w15 | 21 | -0.048286 | -7.854 |
| w16 | 37 | 0.000977 | 26.358 |
| w17 | 13 | -0.165477 | -8.959 |
| w18 | 1 | 0.083744 | 0.422 |
| w19 | 0 | None | 0.0 |
| w21 | 0 | 0.009628 | 0.0 |
| w22 | 0 | -0.166457 | 0.0 |
| w23 | 6 | -0.128413 | -5.754 |
| w24 | 11 | -0.143942 | -7.234 |
| w25 | 13 | -0.16398 | -11.871 |
| w26 | 16 | -0.041198 | -4.398 |
| w27 | 20 | 0.374934 | 100.948 |
| w28 | 20 | -0.022503 | -5.32 |
| w29 | 6 | 0.021088 | 1.763 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 6 | 0.236076 | 16.364 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 0 | None | 0.0 |
| w22 | 15 | -0.030217 | -4.227 |
| w23 | 7 | -0.080922 | -4.659 |
| w24 | 19 | -0.0766 | -4.058 |
| w25 | 9 | -0.102399 | -9.052 |
| w26 | 14 | 0.115196 | 11.685 |
| w27 | 20 | 0.261349 | 119.128 |
| w28 | 12 | 0.002037 | -0.318 |
| w29 | 1 | -0.120371 | -4.057 |
| w30 | 6 | 0.039267 | 0.136 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

