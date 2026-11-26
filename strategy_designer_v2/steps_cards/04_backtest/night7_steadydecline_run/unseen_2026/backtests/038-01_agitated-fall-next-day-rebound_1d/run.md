# Backtest of 038-01_agitated-fall-next-day-rebound_1d

- Plan: `../../../../../03_test_plan/night7_steadydecline_run/plans/038-01_agitated-fall-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.07611 | -25.673 |
| w2 | 14 | -0.036313 | -4.66 |
| w3 | 2 | 0.114591 | 3.272 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.065488 | -16.279 |
| w2 | 6 | -0.068312 | -6.312 |
| w3 | 2 | 0.181935 | 5.479 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.121341 | 5.388 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.099677 | 3.225 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.167217 | 8.957 |
| w2 | 11 | 0.05874 | 3.073 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.283731 | 19.235 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.129857 | 6.029 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.099803 | -15.025 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

