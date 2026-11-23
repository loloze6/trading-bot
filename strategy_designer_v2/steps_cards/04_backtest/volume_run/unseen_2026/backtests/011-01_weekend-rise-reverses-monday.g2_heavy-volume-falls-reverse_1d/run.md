# Backtest of 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d

- Plan: `../../../../../03_test_plan/volume_run/plans/011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.025133 | -18.549 |
| w2 | 9 | -0.062248 | -8.39 |
| w3 | 8 | -0.125562 | -17.23 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.155062 | -26.285 |
| w2 | 7 | -0.234408 | -25.572 |
| w3 | 7 | -0.066763 | -11.439 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.087887 | 2.442 |
| w2 | 7 | -0.017416 | -6.813 |
| w3 | 4 | -0.049788 | -2.66 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.055711 | 2.02 |
| w2 | 8 | 0.140876 | 20.697 |
| w3 | 4 | 0.057419 | 1.765 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.136967 | -26.292 |
| w2 | 12 | -0.156101 | -22.328 |
| w3 | 4 | 0.229183 | 12.067 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.157562 | 9.054 |
| w2 | 6 | -0.112967 | -5.495 |
| w3 | 8 | 0.096016 | 8.098 |

