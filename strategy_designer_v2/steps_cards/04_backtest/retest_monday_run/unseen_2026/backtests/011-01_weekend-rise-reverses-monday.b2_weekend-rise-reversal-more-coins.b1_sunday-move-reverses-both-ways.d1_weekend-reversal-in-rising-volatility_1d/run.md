# Backtest of 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d

- Plan: `../../../../../03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d1_weekend-reversal-in-rising-volatility_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.08228 | 1.654 |
| w2 | 8 | 0.007334 | 3.502 |
| w3 | 4 | 0.087805 | 1.513 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.134351 | 9.854 |
| w2 | 10 | -0.034604 | -1.371 |
| w3 | 3 | 0.043464 | -4.436 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.031144 | -4.167 |
| w2 | 10 | -0.016064 | -4.998 |
| w3 | 8 | -0.00154 | -3.767 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.064859 | -17.421 |
| w2 | 13 | -0.128793 | -9.858 |
| w3 | 10 | -0.097586 | -14.848 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.028478 | -4.873 |
| w2 | 11 | -0.020171 | 1.156 |
| w3 | 3 | 0.060524 | -1.4 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.025444 | 1.623 |
| w2 | 11 | -0.034287 | 0.657 |
| w3 | 6 | 0.151433 | -2.283 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.024775 | -8.505 |
| w2 | 9 | 0.010934 | 2.396 |
| w3 | 4 | -0.05 | -2.549 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.074392 | -9.504 |
| w2 | 11 | 0.051193 | 8.446 |
| w3 | 5 | 0.062135 | -1.264 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.084409 | -0.588 |
| w2 | 14 | 0.047336 | 5.812 |
| w3 | 12 | 0.210542 | 3.398 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.067677 | -1.025 |
| w2 | 8 | 0.052928 | 11.723 |
| w3 | 8 | -0.117301 | -9.923 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.068703 | -0.349 |
| w2 | 12 | 0.013947 | -6.549 |
| w3 | 4 | 0.115997 | 3.205 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.018986 | 2.088 |
| w2 | 10 | 0.056403 | -0.487 |
| w3 | 2 | 0.052287 | -0.89 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.060089 | -11.253 |
| w2 | 11 | 0.061978 | 7.145 |
| w3 | 3 | -0.014842 | -2.169 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.106994 | 2.395 |
| w2 | 10 | -0.104121 | -2.967 |
| w3 | 6 | 0.146899 | -1.943 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.006466 | -11.727 |
| w2 | 16 | 0.028519 | -4.587 |
| w3 | 8 | -0.263554 | -17.128 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.037166 | -1.118 |
| w2 | 14 | -0.032171 | -3.268 |
| w3 | 11 | 0.261697 | 12.167 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.024899 | -2.013 |
| w2 | 7 | 0.152527 | 22.011 |
| w3 | 8 | -0.069683 | -5.024 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.086376 | -6.217 |
| w2 | 10 | -0.000452 | 9.346 |
| w3 | 7 | 0.110992 | 3.27 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.013919 | -7.133 |
| w2 | 10 | -0.021024 | 0.826 |
| w3 | 5 | 0.23469 | 17.109 |

