# Backtest of 034-02_rising-break-swings-continues_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/034-02_rising-break-swings-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.053775 | 1.231 |
| w2 | 5 | 0.131575 | 6.614 |
| w3 | 3 | -0.032796 | -3.94 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.106388 | 0.521 |
| w2 | 2 | 0.079987 | 13.802 |
| w3 | 4 | 0.03104 | 1.4 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.019916 | 0.0 |
| w2 | 4 | -0.114597 | -13.504 |
| w3 | 6 | 0.056903 | 5.724 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.190805 | 10.414 |
| w2 | 10 | 0.052704 | 20.759 |
| w3 | 8 | -0.138398 | -16.962 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.337585 | 7.972 |
| w3 | 2 | 0.032931 | -0.135 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.027319 | 3.086 |
| w2 | 11 | 0.145077 | 42.683 |
| w3 | 8 | -0.027912 | 8.092 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.029346 | -4.774 |
| w3 | 4 | 0.004484 | -0.488 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.0561 | 1.388 |
| w2 | 5 | -0.007673 | -3.653 |
| w3 | 2 | 0.014807 | -1.577 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | -0.027969 | 21.466 |
| w3 | 4 | -0.14059 | -13.278 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.049388 | -2.899 |
| w2 | 11 | 0.04301 | 0.796 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 8 | -0.037507 | 0.468 |
| w3 | 5 | -0.027005 | 6.264 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.165168 | 10.389 |
| w3 | 3 | -0.010698 | -1.818 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.077808 | 0.188 |
| w3 | 4 | 0.291653 | 2.899 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 7 | 0.103852 | 25.661 |
| w3 | 2 | -0.032471 | 2.009 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.006126 | -0.697 |
| w2 | 9 | 0.025122 | 7.442 |
| w3 | 9 | 0.007257 | 0.365 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.092589 | 0.406 |
| w2 | 6 | 0.073434 | 14.257 |
| w3 | 9 | 0.009679 | 17.075 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 5 | 0.126035 | -5.175 |
| w3 | 3 | 0.024006 | 6.689 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.108711 | -0.509 |
| w2 | 5 | -0.096609 | -3.024 |
| w3 | 3 | -0.042561 | -2.824 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 5 | 0.133702 | 28.814 |
| w3 | 4 | -0.029043 | 3.8 |

