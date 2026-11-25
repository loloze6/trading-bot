# Backtest of 034-01.b1_nearness-to-high-10-days_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/034-01.b1_nearness-to-high-10-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.03775 | 1.36 |
| w2 | 7 | 0.139619 | 16.268 |
| w3 | 10 | -0.094233 | -6.063 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.074898 | -0.179 |
| w2 | 7 | 0.168893 | 18.082 |
| w3 | 8 | -0.017078 | 5.587 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.019916 | -1.172 |
| w2 | 7 | -0.146229 | -22.047 |
| w3 | 12 | 0.109049 | 16.328 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.172538 | -8.607 |
| w2 | 15 | 0.031662 | 26.085 |
| w3 | 21 | -0.104519 | -11.266 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | 0.208331 | 4.912 |
| w3 | 8 | 0.01105 | -0.909 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.063954 | 0.875 |
| w2 | 24 | 0.086982 | 33.551 |
| w3 | 13 | 0.01181 | 13.867 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 5 | 0.022853 | -5.519 |
| w3 | 14 | -0.020343 | -4.108 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.0561 | 1.491 |
| w2 | 9 | 0.020313 | -3.857 |
| w3 | 8 | -0.014357 | -4.21 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.076852 | -0.588 |
| w2 | 12 | 0.073488 | 17.303 |
| w3 | 12 | 0.000693 | -14.243 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.044716 | -4.861 |
| w2 | 14 | 0.134257 | -19.739 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.043308 | -1.218 |
| w2 | 12 | 0.081137 | -1.782 |
| w3 | 17 | 0.063992 | 4.081 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | 0.101072 | 6.064 |
| w3 | 10 | 0.022792 | -0.092 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.019669 | -0.451 |
| w2 | 2 | 0.058387 | -2.095 |
| w3 | 10 | 0.181807 | -7.389 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.034978 | -4.594 |
| w2 | 8 | 0.173486 | 21.887 |
| w3 | 9 | 0.005584 | -8.158 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.006095 | -1.493 |
| w2 | 14 | 0.071229 | 19.042 |
| w3 | 13 | -0.175249 | -1.275 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.037661 | -3.296 |
| w2 | 17 | 0.049071 | 17.015 |
| w3 | 14 | 0.173496 | 42.394 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.010791 | -2.063 |
| w2 | 7 | 0.098779 | -8.26 |
| w3 | 11 | 0.146988 | 13.847 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.028862 | -0.77 |
| w2 | 6 | -0.021294 | -5.513 |
| w3 | 11 | -0.019299 | -12.519 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.128754 | 0.0 |
| w2 | 14 | 0.005643 | 11.971 |
| w3 | 9 | -0.041756 | 10.931 |

