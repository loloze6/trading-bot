# Backtest of 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d

- Plan: `../../../../../03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.005995 | -2.253 |
| w2 | 11 | 0.120121 | -5.285 |
| w3 | 4 | -0.047991 | -3.398 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.052758 | -3.275 |
| w2 | 8 | 0.037119 | -1.419 |
| w3 | 4 | 0.008111 | -3.038 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 17 | -0.040202 | -37.9 |
| w3 | 9 | 0.126085 | 18.556 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.084948 | -8.737 |
| w2 | 12 | 0.076157 | 44.78 |
| w3 | 11 | -0.143631 | 10.459 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.032375 | -9.628 |
| w2 | 13 | 0.065612 | -18.011 |
| w3 | 3 | -0.094849 | -2.716 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.103992 | -21.961 |
| w2 | 14 | 0.049677 | 55.841 |
| w3 | 7 | 0.010156 | 3.681 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.043445 | -8.87 |
| w2 | 12 | -0.128606 | -53.392 |
| w3 | 2 | 0.032297 | 0.176 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.046555 | -0.092 |
| w2 | 7 | 0.112665 | 1.863 |
| w3 | 3 | -0.050767 | -11.455 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.044795 | 9.898 |
| w2 | 14 | 0.084739 | 13.699 |
| w3 | 6 | 0.034705 | -9.464 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.092405 | 11.626 |
| w2 | 16 | -0.098203 | -14.776 |
| w3 | 5 | -0.241295 | -20.603 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.106648 | 0.133 |
| w2 | 11 | 0.035329 | 18.404 |
| w3 | 4 | 0.061527 | 1.748 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.0112 | -21.063 |
| w2 | 5 | -0.009091 | 33.185 |
| w3 | 4 | -0.012827 | 4.454 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.048974 | -24.355 |
| w2 | 6 | -0.004532 | -16.092 |
| w3 | 3 | 0.029991 | 2.837 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.025614 | -7.387 |
| w2 | 10 | 0.024534 | 11.833 |
| w3 | 1 | 0.133618 | 7.627 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.130384 | -30.231 |
| w2 | 8 | -0.067347 | 33.199 |
| w3 | 4 | -0.151399 | -13.734 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.110539 | 0.347 |
| w2 | 9 | 0.013489 | 19.704 |
| w3 | 7 | 0.126579 | 53.702 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.007018 | -3.365 |
| w2 | 3 | -0.018153 | -13.531 |
| w3 | 5 | 0.223513 | 20.549 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.143961 | 13.493 |
| w2 | 10 | 0.000999 | -19.798 |
| w3 | 4 | -0.096033 | -3.904 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.012218 | -3.082 |
| w2 | 7 | -0.046022 | -1.589 |
| w3 | 4 | 0.142368 | 13.497 |

