# Backtest of 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d

- Plan: `../../../../../03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.054898 | 26.354 |
| w2 | 30 | -0.264109 | -58.978 |
| w3 | 20 | -0.271036 | -17.446 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.023861 | 47.318 |
| w2 | 28 | -0.034003 | -56.12 |
| w3 | 23 | -0.185122 | -27.055 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.014554 | 61.861 |
| w2 | 31 | -0.170678 | -41.678 |
| w3 | 18 | -0.0592 | 0.764 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.209465 | 48.217 |
| w2 | 44 | -0.170286 | -22.715 |
| w3 | 21 | -0.170013 | -10.435 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.060642 | 38.046 |
| w2 | 34 | -0.343854 | -55.912 |
| w3 | 12 | -0.13159 | -9.388 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.160039 | -27.248 |
| w2 | 29 | 0.038237 | -45.07 |
| w3 | 21 | 0.006556 | 21.335 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.039362 | 51.493 |
| w2 | 24 | -0.305545 | -50.396 |
| w3 | 16 | 0.208266 | 13.446 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.02661 | 39.047 |
| w2 | 23 | -0.254594 | -39.851 |
| w3 | 20 | -0.108488 | -11.644 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | 0.004994 | 57.774 |
| w2 | 37 | -0.048057 | -54.432 |
| w3 | 24 | -0.049053 | 0.523 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.037179 | -4.154 |
| w2 | 42 | -0.026787 | -1.639 |
| w3 | 22 | -0.245199 | -25.034 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.085137 | 36.734 |
| w2 | 31 | -0.051469 | -29.517 |
| w3 | 14 | -0.09252 | 15.255 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.021636 | 42.299 |
| w2 | 21 | 0.100555 | 20.244 |
| w3 | 18 | 0.14688 | 23.14 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.064706 | 49.262 |
| w2 | 31 | -0.101265 | -33.271 |
| w3 | 12 | 0.180459 | 21.411 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.01299 | 56.388 |
| w2 | 37 | -0.021687 | -65.872 |
| w3 | 13 | -0.135992 | -6.708 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.004468 | 17.282 |
| w2 | 23 | -0.102245 | 47.02 |
| w3 | 16 | -0.132568 | 3.626 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.045165 | 8.767 |
| w2 | 25 | 0.121662 | 86.622 |
| w3 | 24 | 0.055013 | 71.667 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.014687 | 41.483 |
| w2 | 28 | 0.063293 | -56.839 |
| w3 | 17 | 0.032019 | -18.445 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.077799 | -34.414 |
| w2 | 29 | -0.038207 | -10.69 |
| w3 | 19 | -0.007146 | 5.896 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.035314 | 49.778 |
| w2 | 32 | 0.123101 | 4.147 |
| w3 | 19 | 0.014764 | -35.648 |

