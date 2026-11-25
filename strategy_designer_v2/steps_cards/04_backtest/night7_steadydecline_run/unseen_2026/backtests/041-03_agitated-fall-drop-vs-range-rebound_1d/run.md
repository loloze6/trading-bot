# Backtest of 041-03_agitated-fall-drop-vs-range-rebound_1d

- Plan: `../../../../../03_test_plan/night7_steadydecline_run/plans/041-03_agitated-fall-drop-vs-range-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.076395 | -26.755 |
| w2 | 13 | -0.048228 | -7.027 |
| w3 | 2 | 0.113482 | 3.28 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.066854 | -18.826 |
| w2 | 4 | -0.068397 | -7.572 |
| w3 | 2 | 0.181234 | 5.487 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.088872 | 3.132 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.102604 | 3.767 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.126184 | 8.531 |
| w2 | 11 | 0.055854 | 3.931 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.242379 | 18.747 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.134737 | 6.725 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.16356 | -29.531 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

