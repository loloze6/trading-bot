# Backtest of 064-01_falling-agitated-heavy-volume-fall-rebound_1d

- Plan: `../../../../../03_test_plan/night8_choppyagitated_run/plans/064-01_falling-agitated-heavy-volume-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.099776 | -23.697 |
| w2 | 5 | 0.007971 | 0.251 |
| w3 | 2 | 0.113238 | 3.281 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.092082 | -15.659 |
| w2 | 3 | -0.125831 | -5.753 |
| w3 | 1 | 0.180803 | 5.52 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.213938 | 7.96 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.079344 | 1.521 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.083383 | 0.846 |
| w2 | 1 | 0.082617 | 3.03 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.483523 | 20.713 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.145995 | 6.622 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.032573 | 1.767 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.015362 | -1.701 |
| w2 | 4 | -0.034533 | -3.37 |
| w3 | 0 | None | 0.0 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.031374 | 0.755 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.07566 | 0.491 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.114247 | -2.336 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | 0.015473 | -0.369 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.14467 | -6.214 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.084026 | 3.836 |
| w2 | 1 | 0.062969 | 0.576 |
| w3 | 0 | 0.245129 | 0.0 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.055949 | -3.094 |
| w2 | 3 | 0.03474 | 0.598 |
| w3 | 0 | None | 0.0 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.011727 | -6.415 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.122524 | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.094896 | 5.145 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.263151 | 12.481 |
| w2 | 2 | -0.040936 | -1.657 |
| w3 | 0 | None | 0.0 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.067029 | 2.445 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.082363 | 2.732 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.116747 | 4.773 |

