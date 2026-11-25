# Backtest of 048-01_scaled-up-week-continuation_1d

- Plan: `../../../../../03_test_plan/night7_panic_run/plans/048-01_scaled-up-week-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | 0.032294 | -8.849 |
| w2 | 41 | 0.161294 | 25.975 |
| w3 | 10 | -0.007511 | -6.933 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.012662 | -13.318 |
| w2 | 39 | 0.097271 | 22.938 |
| w3 | 10 | -0.014415 | -8.843 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | 0.018876 | -12.249 |
| w2 | 35 | 0.082364 | -0.848 |
| w3 | 18 | 0.167826 | 21.3 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | 0.081475 | 12.344 |
| w2 | 51 | -0.038499 | 22.678 |
| w3 | 29 | -0.017546 | -4.953 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.069636 | 7.391 |
| w2 | 35 | 0.136254 | 22.772 |
| w3 | 12 | -0.003038 | -3.848 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.047334 | 3.865 |
| w2 | 45 | 0.077013 | 49.559 |
| w3 | 23 | -0.0657 | -2.779 |

