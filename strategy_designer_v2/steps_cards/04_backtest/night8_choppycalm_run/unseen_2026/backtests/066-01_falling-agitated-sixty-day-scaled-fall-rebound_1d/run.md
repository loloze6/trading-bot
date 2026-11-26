# Backtest of 066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d

- Plan: `../../../../../03_test_plan/night8_choppycalm_run/plans/066-01_falling-agitated-sixty-day-scaled-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.108108 | -24.804 |
| w2 | 11 | -0.025681 | -2.722 |
| w3 | 1 | 0.113962 | 3.342 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.040968 | -10.703 |
| w2 | 6 | -0.076311 | -5.595 |
| w3 | 1 | 0.181065 | 5.52 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.229014 | 9.707 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.084142 | 2.413 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.185538 | 6.495 |
| w2 | 3 | 0.023017 | 0.057 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.501417 | 20.959 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.108292 | 4.764 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.039517 | -7.349 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.070273 | 2.423 |
| w2 | 9 | -0.025554 | -3.143 |
| w3 | 0 | None | 0.0 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.039088 | -1.58 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.07566 | 0.0 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.010243 | -0.544 |
| w2 | 0 | None | 0.0 |
| w3 | 6 | 0.123413 | 5.372 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.001076 | -0.958 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.033295 | 0.87 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.116424 | 6.91 |
| w2 | 1 | 0.001751 | -0.254 |
| w3 | 1 | 0.245565 | 7.967 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.026766 | -1.862 |
| w2 | 3 | 0.197089 | 2.879 |
| w3 | 0 | None | 0.0 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.048311 | -9.227 |
| w2 | 0 | 0.127224 | 0.0 |
| w3 | 0 | 0.199043 | 0.0 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.098935 | -3.354 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.095565 | -2.407 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.269109 | 12.3 |
| w2 | 1 | -0.094575 | -5.418 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.085206 | 1.786 |
| w2 | 0 | 0.006156 | 0.0 |
| w3 | 0 | None | 0.0 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.128887 | 6.454 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.1169 | 5.455 |

