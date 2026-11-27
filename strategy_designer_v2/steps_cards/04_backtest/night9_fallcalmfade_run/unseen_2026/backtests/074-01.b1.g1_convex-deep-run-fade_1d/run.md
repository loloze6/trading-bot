# Backtest of 074-01.b1.g1_convex-deep-run-fade_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.g1_convex-deep-run-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.040162 | 5.596 |
| w2 | 4 | -0.0146 | -1.003 |
| w3 | 1 | 0.030894 | 1.316 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.054751 | 5.088 |
| w2 | 2 | 0.001438 | 0.034 |
| w3 | 4 | 0.039105 | 2.88 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.03116 | 4.084 |
| w2 | 5 | 0.043114 | 3.029 |
| w3 | 1 | 0.075502 | 2.393 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.023641 | -1.833 |
| w2 | 0 | 0.014812 | 0.0 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.065824 | 5.938 |
| w2 | 7 | -0.001343 | -1.242 |
| w3 | 1 | 0.056514 | 2.412 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.15575 | -12.925 |
| w2 | 1 | 0.001364 | -0.141 |
| w3 | 1 | 0.029527 | 0.874 |

