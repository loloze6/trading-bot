# Backtest of 031-01.b1.b1_wide-day-extends-run-more-coins_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.b1_wide-day-extends-run-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.023699 | -3.627 |
| w2 | 46 | 0.202424 | 32.059 |
| w3 | 19 | -0.197199 | -15.454 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 49 | -0.101014 | -25.273 |
| w2 | 42 | 0.176571 | 38.531 |
| w3 | 20 | -0.151915 | -12.856 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.06604 | -20.728 |
| w2 | 43 | 0.11179 | -7.04 |
| w3 | 27 | 0.084681 | 11.661 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.041218 | 2.513 |
| w2 | 61 | -0.138243 | -8.602 |
| w3 | 30 | -0.070043 | -1.97 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.022014 | -9.169 |
| w2 | 39 | 0.194661 | 32.432 |
| w3 | 17 | -0.229594 | -22.675 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.014354 | -4.103 |
| w2 | 48 | 0.223431 | 107.492 |
| w3 | 32 | 0.099571 | 16.917 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.184106 | -31.493 |
| w2 | 44 | 0.260485 | 55.927 |
| w3 | 20 | -0.053927 | -6.245 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.088839 | -18.092 |
| w2 | 33 | 0.101564 | 5.592 |
| w3 | 22 | -0.088624 | -7.101 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.125089 | -25.489 |
| w2 | 55 | 0.097676 | 28.823 |
| w3 | 24 | -0.060241 | -5.418 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 67 | -0.076736 | 18.248 |
| w2 | 59 | 0.130975 | 12.636 |
| w3 | 25 | -0.387316 | -17.139 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.194056 | -25.702 |
| w2 | 45 | 0.144966 | 73.517 |
| w3 | 34 | 0.046147 | 9.752 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.083326 | -10.768 |
| w2 | 38 | 0.108528 | 53.523 |
| w3 | 21 | 0.115363 | 11.362 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.104733 | -23.224 |
| w2 | 41 | 0.008966 | 1.976 |
| w3 | 26 | 0.111969 | 26.377 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.026463 | -11.876 |
| w2 | 45 | 0.235296 | 71.897 |
| w3 | 18 | -0.00346 | -2.881 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | -0.045771 | -14.071 |
| w2 | 48 | -0.054315 | 6.08 |
| w3 | 29 | -0.120811 | 1.869 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.020432 | -7.455 |
| w2 | 33 | 0.082552 | 55.916 |
| w3 | 35 | 0.170947 | 56.888 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.011303 | -13.404 |
| w2 | 49 | 0.199361 | 41.636 |
| w3 | 21 | 0.141647 | 24.315 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | 0.069574 | 11.964 |
| w2 | 41 | 0.108121 | 29.815 |
| w3 | 19 | 0.056301 | 8.247 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.167014 | -29.915 |
| w2 | 41 | 0.11813 | 70.703 |
| w3 | 22 | 0.087023 | 8.527 |

