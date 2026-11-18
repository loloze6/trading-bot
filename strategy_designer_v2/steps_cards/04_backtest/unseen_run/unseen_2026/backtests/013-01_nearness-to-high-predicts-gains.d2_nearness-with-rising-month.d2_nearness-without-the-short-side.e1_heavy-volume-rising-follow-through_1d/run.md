# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d

- Plan: `../../../../../03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 46 | -0.00863 | -9.361 |
| w2 | 42 | 0.092789 | 11.928 |
| w3 | 37 | 0.045921 | -4.989 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 54 | -0.098963 | -26.595 |
| w2 | 50 | 0.131469 | 28.38 |
| w3 | 31 | 0.052915 | -5.414 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.057924 | -16.111 |
| w2 | 38 | 0.049057 | -0.216 |
| w3 | 29 | 0.262183 | 39.6 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.047084 | -11.542 |
| w2 | 52 | -0.018895 | 9.588 |
| w3 | 50 | 0.056175 | 3.642 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.084612 | -22.041 |
| w2 | 27 | 0.065286 | 4.295 |
| w3 | 21 | -0.057387 | -10.133 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | 0.031461 | 2.743 |
| w2 | 58 | 0.058469 | 48.96 |
| w3 | 26 | 0.07175 | 11.163 |

