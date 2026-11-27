# Backtest of 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d

- Plan: `../../../../../03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.045119 | 5.997 |
| w2 | 9 | 0.038635 | 1.319 |
| w3 | 2 | 0.030894 | 0.989 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.006414 | 1.593 |
| w2 | 10 | 0.025226 | 0.781 |
| w3 | 5 | 0.128992 | 6.832 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.046905 | -1.797 |
| w2 | 9 | 0.044202 | 2.905 |
| w3 | 2 | 0.075502 | 1.408 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.006539 | 0.037 |
| w2 | 7 | 0.022323 | -0.257 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.054876 | 4.252 |
| w2 | 17 | 0.050686 | 2.371 |
| w3 | 3 | 0.009376 | 0.478 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.090933 | -6.55 |
| w2 | 2 | -0.00828 | -0.457 |
| w3 | 1 | 0.029527 | 0.432 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.077393 | -6.253 |
| w2 | 10 | -0.008537 | -1.057 |
| w3 | 6 | 0.045512 | 1.573 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.011361 | -1.18 |
| w2 | 15 | -0.141576 | -10.554 |
| w3 | 5 | 0.061043 | 2.9 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.012772 | 0.18 |
| w2 | 10 | -0.087398 | -7.725 |
| w3 | 3 | 0.041561 | 0.995 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.058583 | 6.618 |
| w2 | 6 | -0.09218 | -7.695 |
| w3 | 2 | 0.008469 | 0.025 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.100489 | -8.123 |
| w2 | 9 | 0.107599 | 4.96 |
| w3 | 1 | None | -0.024 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.069707 | -3.767 |
| w2 | 13 | -0.091277 | -5.765 |
| w3 | 1 | None | -0.045 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.035751 | 0.099 |
| w2 | 9 | 0.054917 | 1.304 |
| w3 | 4 | 0.119138 | 5.28 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.037828 | -3.818 |
| w2 | 3 | -0.172991 | -12.135 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.000964 | 0.176 |
| w2 | 8 | 0.077276 | 2.131 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.01389 | 0.285 |
| w2 | 10 | -0.037736 | -1.913 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.020887 | 0.231 |
| w2 | 17 | 0.137022 | 8.257 |
| w3 | 3 | 0.0338 | 0.647 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.08245 | -4.673 |
| w2 | 3 | -0.242198 | -8.136 |
| w3 | 1 | None | -0.042 |

