# Backtest of 031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | 0.021792 | 1.68 |
| w2 | 48 | 0.191001 | 32.68 |
| w3 | 18 | -0.149577 | -9.915 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 54 | -0.076241 | -24.158 |
| w2 | 53 | 0.210616 | 42.716 |
| w3 | 17 | -0.204103 | -16.017 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.083526 | -17.922 |
| w2 | 37 | 0.13844 | 13.042 |
| w3 | 24 | 0.091665 | 10.097 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | 0.011755 | 6.863 |
| w2 | 60 | -0.104229 | -5.016 |
| w3 | 29 | -0.023882 | 4.523 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | 0.005601 | -2.545 |
| w2 | 37 | 0.217705 | 40.431 |
| w3 | 18 | -0.289958 | -23.857 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | 0.051138 | 0.787 |
| w2 | 42 | 0.187635 | 75.713 |
| w3 | 31 | 0.007397 | 4.315 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.082704 | -21.773 |
| w2 | 43 | 0.247649 | 53.94 |
| w3 | 21 | -0.03279 | -5.59 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.107212 | -14.515 |
| w2 | 36 | 0.136203 | 11.527 |
| w3 | 16 | -0.094696 | -6.398 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.125367 | -23.0 |
| w2 | 55 | 0.152767 | 40.555 |
| w3 | 21 | -0.020184 | -3.798 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 65 | -0.122538 | 13.867 |
| w2 | 61 | 0.117592 | 12.871 |
| w3 | 20 | -0.266994 | -22.55 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.206467 | -17.848 |
| w2 | 50 | 0.162689 | 74.19 |
| w3 | 30 | 0.041459 | 7.565 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.106817 | -17.947 |
| w2 | 34 | 0.103389 | 50.875 |
| w3 | 21 | 0.157228 | 7.123 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.097572 | -21.217 |
| w2 | 46 | 0.098869 | 1.847 |
| w3 | 23 | 0.03997 | 17.679 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.03132 | -7.158 |
| w2 | 49 | 0.19921 | 56.692 |
| w3 | 14 | -0.084702 | -6.352 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.019272 | -3.302 |
| w2 | 46 | -0.048095 | 13.684 |
| w3 | 30 | -0.036584 | 14.071 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.002737 | -7.014 |
| w2 | 31 | 0.028927 | 45.863 |
| w3 | 28 | 0.182606 | 68.875 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | 0.018287 | -3.481 |
| w2 | 47 | 0.17183 | 38.405 |
| w3 | 16 | 0.163952 | 22.216 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | 0.118273 | 22.453 |
| w2 | 41 | 0.077047 | 16.875 |
| w3 | 21 | 0.060725 | -2.035 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.073159 | -18.097 |
| w2 | 50 | 0.12983 | 76.476 |
| w3 | 18 | 0.115452 | 12.285 |

