# Backtest of 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b1_near-high-momentum-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.022891 | -13.599 |
| w2 | 34 | 0.078283 | -18.808 |
| w3 | 13 | 0.001404 | -6.308 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.033919 | -17.307 |
| w2 | 34 | 0.097561 | 36.562 |
| w3 | 14 | 0.010715 | 1.235 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.045294 | 25.472 |
| w2 | 37 | -0.044417 | -45.781 |
| w3 | 21 | 0.153911 | 21.374 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.054218 | 21.486 |
| w2 | 28 | 0.056887 | 48.545 |
| w3 | 17 | -0.032906 | -12.707 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 49 | -0.16956 | -44.979 |
| w2 | 41 | 0.02668 | -30.937 |
| w3 | 9 | -0.090595 | -4.843 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.144818 | 25.673 |
| w2 | 27 | 0.107584 | -11.655 |
| w3 | 13 | 0.031358 | 12.597 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 59 | -0.190255 | -12.463 |
| w2 | 33 | 0.096301 | 13.719 |
| w3 | 11 | -0.04901 | 0.406 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 55 | -0.105206 | -9.8 |
| w2 | 30 | 0.116008 | -28.188 |
| w3 | 11 | -0.16102 | -9.35 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | -0.232487 | -34.63 |
| w2 | 30 | 0.150918 | 60.031 |
| w3 | 10 | 0.120098 | 10.107 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.075368 | 20.934 |
| w2 | 31 | 0.051597 | -3.445 |
| w3 | 33 | -0.374472 | -3.131 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | -0.034497 | 7.681 |
| w2 | 34 | -0.059391 | 11.074 |
| w3 | 10 | 0.160768 | 21.138 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | -0.191869 | -14.007 |
| w2 | 34 | -0.035205 | -16.118 |
| w3 | 14 | -0.00716 | 15.119 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | -0.200956 | -26.098 |
| w2 | 45 | 0.031868 | -19.431 |
| w3 | 14 | 0.139077 | 22.026 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.156501 | -26.098 |
| w2 | 36 | 0.076352 | 33.392 |
| w3 | 16 | -0.039716 | -6.666 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.111574 | -0.802 |
| w2 | 26 | -0.044615 | 18.815 |
| w3 | 18 | -0.111828 | 13.172 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.08228 | -21.7 |
| w2 | 30 | -0.03788 | 6.356 |
| w3 | 20 | 0.039546 | 108.333 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.122438 | -36.634 |
| w2 | 31 | -0.0364 | -33.395 |
| w3 | 17 | 0.193955 | 18.012 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | 0.013087 | 2.805 |
| w2 | 26 | 0.0146 | 14.218 |
| w3 | 10 | -0.058064 | -2.961 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 57 | -0.112391 | -16.405 |
| w2 | 16 | 0.107218 | 8.922 |
| w3 | 10 | 0.025834 | 11.936 |

