# Backtest of 058-03.e1_calm-rise-stretch-ten-days_1d

- Plan: `../../../../../03_test_plan/night8_risingagitated_run/plans/058-03.e1_calm-rise-stretch-ten-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.066904 | -3.454 |
| w2 | 7 | 0.160236 | 9.285 |
| w3 | 4 | 0.14521 | 0.703 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.024519 | -0.121 |
| w2 | 6 | 0.289469 | 15.909 |
| w3 | 9 | 0.069288 | -1.787 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.019916 | -2.828 |
| w2 | 8 | -0.155551 | -32.895 |
| w3 | 3 | 0.126733 | 8.252 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.074395 | 8.769 |
| w2 | 18 | 0.100356 | 59.311 |
| w3 | 18 | -0.033739 | -2.755 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.215604 | 7.438 |
| w2 | 13 | 0.120465 | 66.341 |
| w3 | 5 | 0.254411 | 15.346 |

