# Backtest of 034-01.e1_rising-market-breakout-distance-continuation_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/034-01.e1_rising-market-breakout-distance-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.053775 | -0.781 |
| w2 | 5 | 0.131575 | 4.736 |
| w3 | 3 | -0.032796 | -3.403 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.106388 | -0.459 |
| w2 | 2 | 0.079987 | 10.949 |
| w3 | 4 | 0.03104 | 1.413 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.019916 | 0.0 |
| w2 | 4 | -0.114597 | -11.897 |
| w3 | 8 | 0.056903 | 12.171 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.190805 | 17.075 |
| w2 | 13 | 0.052704 | 16.504 |
| w3 | 9 | -0.138398 | -15.834 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | 0.337585 | 10.671 |
| w3 | 2 | 0.032931 | -0.038 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.027319 | 4.139 |
| w2 | 14 | 0.145077 | 42.279 |
| w3 | 7 | -0.027912 | 9.459 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.029346 | -2.209 |
| w3 | 4 | 0.004484 | -4.68 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.0561 | 1.388 |
| w2 | 5 | -0.007673 | -3.727 |
| w3 | 2 | 0.014807 | -2.052 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | -0.027969 | 13.316 |
| w3 | 4 | -0.14059 | -10.523 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.049388 | -3.782 |
| w2 | 17 | 0.04301 | -2.145 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | -0.037507 | 3.348 |
| w3 | 7 | -0.027005 | 12.937 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.165168 | 14.335 |
| w3 | 5 | -0.010698 | -1.601 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.077808 | 3.702 |
| w3 | 5 | 0.291653 | 12.979 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 9 | 0.103852 | 17.296 |
| w3 | 3 | -0.032471 | 1.031 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.006126 | -0.697 |
| w2 | 12 | 0.025122 | 7.142 |
| w3 | 8 | 0.007257 | -0.539 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.092589 | -0.126 |
| w2 | 6 | 0.073434 | 14.794 |
| w3 | 10 | 0.009679 | 13.889 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 5 | 0.126035 | 2.407 |
| w3 | 5 | 0.024006 | -1.974 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.108711 | -0.438 |
| w2 | 5 | -0.096609 | -3.87 |
| w3 | 2 | -0.042561 | -5.524 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | 0.133702 | 37.767 |
| w3 | 5 | -0.029043 | 0.158 |

