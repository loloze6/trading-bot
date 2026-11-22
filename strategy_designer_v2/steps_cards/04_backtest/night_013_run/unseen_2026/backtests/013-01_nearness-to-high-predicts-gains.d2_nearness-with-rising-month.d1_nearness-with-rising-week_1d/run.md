# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d

- Plan: `../../../../../03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | 0.008751 | 1.457 |
| w2 | 25 | 0.110893 | 12.174 |
| w3 | 14 | -0.0994 | -4.476 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.079339 | -3.911 |
| w2 | 23 | -0.040708 | -4.976 |
| w3 | 16 | 0.069705 | 2.244 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.045325 | 1.597 |
| w2 | 30 | -0.050649 | -4.33 |
| w3 | 21 | 0.141683 | 13.359 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.079959 | 9.99 |
| w2 | 36 | 0.053069 | 17.301 |
| w3 | 36 | -0.005462 | -1.685 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.062733 | 5.223 |
| w2 | 22 | 0.000513 | 0.491 |
| w3 | 13 | -0.006475 | -0.997 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.08456 | 4.474 |
| w2 | 34 | 0.028643 | 13.539 |
| w3 | 20 | 0.123985 | 13.606 |

