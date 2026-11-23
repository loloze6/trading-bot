# Backtest of 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d

- Plan: `../../../../../03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.24695 | 16.525 |
| w2 | 2 | 0.055189 | -4.652 |
| w3 | 0 | 0.377318 | 0.0 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.096907 | -7.67 |
| w2 | 4 | 0.066533 | -2.001 |
| w3 | 0 | None | 0.0 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.111991 | 3.827 |
| w2 | 1 | 0.051099 | 1.891 |
| w3 | 2 | 0.030563 | -3.793 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.06222 | 1.195 |
| w2 | 0 | -0.125215 | 0.0 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.022221 | -2.698 |
| w2 | 1 | 0.047387 | 1.722 |
| w3 | 0 | -0.033911 | 0.0 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.003419 | -4.496 |
| w2 | 2 | 0.012404 | -1.455 |
| w3 | 2 | 0.105412 | -1.051 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.014787 | -0.279 |
| w2 | 6 | 0.048333 | -4.439 |
| w3 | 0 | None | 0.0 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.047002 | 0.009 |
| w2 | 1 | 0.035037 | 1.042 |
| w3 | 0 | None | 0.0 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.012402 | -0.137 |
| w2 | 1 | 0.038476 | 1.451 |
| w3 | 5 | 0.093325 | -3.756 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.039581 | -0.427 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.005798 | 0.246 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.075233 | 2.649 |
| w2 | 0 | -0.008213 | 0.0 |
| w3 | 4 | 0.126816 | 1.082 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.000927 | 3.654 |
| w2 | 5 | 0.017406 | 1.891 |
| w3 | 0 | 0.078264 | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.070733 | -0.395 |
| w2 | 2 | 0.065069 | 2.059 |
| w3 | 0 | 0.00338 | 0.0 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.116341 | 1.773 |
| w2 | 1 | 0.030399 | 1.686 |
| w3 | 0 | None | 0.0 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.089278 | -7.729 |
| w2 | 5 | 0.075445 | -5.421 |
| w3 | 0 | 0.063578 | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.010024 | 0.181 |
| w2 | 3 | 0.0373 | -4.195 |
| w3 | 4 | 0.064424 | 4.403 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.022414 | -5.239 |
| w2 | 3 | 0.060279 | -1.947 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.031322 | -2.919 |
| w2 | 0 | 0.032208 | 0.0 |
| w3 | 0 | 0.307534 | 0.0 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.010194 | -4.451 |
| w2 | 3 | -0.029071 | 1.507 |
| w3 | 2 | 0.135636 | 0.747 |

