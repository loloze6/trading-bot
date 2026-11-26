# Backtest of 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d

- Plan: `../../../../../03_test_plan/night6_streak_run/plans/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.075673 | -13.795 |
| w2 | 20 | 0.07904 | 21.161 |
| w3 | 15 | 0.120471 | 3.059 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.114423 | -22.532 |
| w2 | 22 | 0.05097 | 7.516 |
| w3 | 11 | 0.1533 | 3.827 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.067201 | -4.287 |
| w2 | 19 | -0.086926 | -15.182 |
| w3 | 12 | 0.197965 | 37.645 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.019886 | 4.909 |
| w2 | 30 | 0.077712 | 49.041 |
| w3 | 17 | -0.0167 | -4.665 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.155079 | -27.12 |
| w2 | 12 | -0.00403 | 1.872 |
| w3 | 8 | 0.068016 | -3.786 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.071593 | 8.804 |
| w2 | 27 | 0.070123 | 51.416 |
| w3 | 8 | 0.225542 | 47.236 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.220934 | -10.167 |
| w2 | 23 | -0.093585 | -19.0 |
| w3 | 16 | -0.017829 | -1.421 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.002897 | -0.762 |
| w2 | 14 | -0.006207 | -10.697 |
| w3 | 10 | 0.044127 | -1.697 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.150502 | -18.277 |
| w2 | 28 | 0.085884 | 40.294 |
| w3 | 20 | 0.069882 | -0.535 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.037489 | 13.583 |
| w2 | 29 | -0.067279 | -0.092 |
| w3 | 12 | -0.18028 | -24.196 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.133951 | -18.633 |
| w2 | 32 | -0.034049 | 19.417 |
| w3 | 14 | 0.209683 | 35.381 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.15205 | -14.651 |
| w2 | 18 | -0.035291 | -0.064 |
| w3 | 17 | 0.079015 | 2.847 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.187415 | -18.294 |
| w2 | 12 | -0.028385 | -4.85 |
| w3 | 18 | 0.188989 | 41.969 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.17341 | -33.565 |
| w2 | 19 | 0.032912 | 15.104 |
| w3 | 13 | 0.178206 | 9.59 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.061358 | -9.356 |
| w2 | 15 | 0.050158 | 28.321 |
| w3 | 23 | 0.060642 | 36.645 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.168062 | -27.341 |
| w2 | 15 | 0.033476 | 66.562 |
| w3 | 18 | 0.220587 | 126.718 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.147408 | -25.238 |
| w2 | 21 | -0.042667 | -19.477 |
| w3 | 23 | 0.063909 | 16.574 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.060792 | 4.788 |
| w2 | 10 | 0.000284 | 1.915 |
| w3 | 18 | 0.096892 | 13.31 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.058506 | -0.354 |
| w2 | 21 | 0.012937 | 29.192 |
| w3 | 14 | -0.031726 | 12.946 |

