# Backtest of 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d

- Plan: `../../../../../03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.08319 | 1.627 |
| w2 | 5 | 0.213458 | 18.946 |
| w3 | 3 | 0.134805 | 10.299 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.030978 | 3.041 |
| w2 | 8 | 0.037134 | 5.766 |
| w3 | 3 | 0.252931 | 10.128 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.053034 | 2.33 |
| w2 | 8 | -0.11287 | -9.306 |
| w3 | 6 | 0.031798 | -8.052 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.228329 | 10.515 |
| w2 | 6 | -0.082099 | 0.136 |
| w3 | 6 | -0.141623 | -14.822 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.020866 | -3.07 |
| w2 | 9 | 0.012022 | -7.078 |
| w3 | 2 | 0.093192 | -3.796 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.030168 | 12.764 |
| w2 | 9 | 0.078125 | 1.212 |
| w3 | 4 | 0.08792 | 20.884 |

