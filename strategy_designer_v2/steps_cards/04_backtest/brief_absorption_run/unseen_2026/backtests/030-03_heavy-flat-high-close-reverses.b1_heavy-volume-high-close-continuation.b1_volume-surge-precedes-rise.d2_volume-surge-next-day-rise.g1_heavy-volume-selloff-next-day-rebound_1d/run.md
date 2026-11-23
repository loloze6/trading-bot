# Backtest of 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d

- Plan: `../../../../../03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.10666 | -30.444 |
| w2 | 22 | -0.159921 | -22.95 |
| w3 | 19 | -0.086628 | -14.256 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.07136 | -20.926 |
| w2 | 27 | -0.135309 | -21.232 |
| w3 | 13 | -0.038349 | -10.563 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.000716 | -9.85 |
| w2 | 24 | -0.044962 | -12.55 |
| w3 | 11 | 0.097076 | 6.54 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.071858 | 7.696 |
| w2 | 19 | 0.04338 | 9.431 |
| w3 | 17 | 0.047201 | -2.131 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.084157 | -23.686 |
| w2 | 26 | -0.136612 | -25.721 |
| w3 | 12 | 0.077314 | -0.644 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.004391 | -3.148 |
| w2 | 17 | 0.018477 | 6.589 |
| w3 | 15 | 0.194684 | 16.8 |

