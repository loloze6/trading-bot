# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d

- Plan: `../../../../../03_test_plan/hold2_rerun_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | -0.00863 | -14.045 |
| w2 | 46 | 0.092789 | 11.241 |
| w3 | 40 | 0.045921 | 2.588 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | -0.098963 | -26.808 |
| w2 | 52 | 0.131469 | 32.826 |
| w3 | 31 | 0.052915 | -3.502 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.057924 | -15.25 |
| w2 | 42 | 0.049057 | -1.983 |
| w3 | 33 | 0.262183 | 32.701 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.047084 | -5.744 |
| w2 | 55 | -0.018895 | 17.557 |
| w3 | 48 | 0.056175 | 1.382 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.084612 | -19.044 |
| w2 | 30 | 0.065286 | -1.434 |
| w3 | 21 | -0.057387 | -4.721 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | 0.031461 | 0.855 |
| w2 | 56 | 0.058469 | 61.985 |
| w3 | 27 | 0.07175 | 21.069 |

