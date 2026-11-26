# Backtest of 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.081411 | -19.771 |
| w2 | 6 | 0.000875 | -0.297 |
| w3 | 6 | 0.103933 | 2.714 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.211567 | 13.297 |
| w2 | 3 | 0.058811 | 1.544 |
| w3 | 4 | 0.09863 | 0.955 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 10 | -0.013512 | -2.861 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.034958 | -0.451 |
| w2 | 8 | -0.139177 | -1.888 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.416463 | 19.61 |
| w2 | 4 | -0.004122 | -0.692 |
| w3 | 7 | 0.094436 | 1.462 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.024643 | -2.003 |
| w2 | 9 | -0.1393 | -6.413 |
| w3 | 0 | None | 0.0 |

