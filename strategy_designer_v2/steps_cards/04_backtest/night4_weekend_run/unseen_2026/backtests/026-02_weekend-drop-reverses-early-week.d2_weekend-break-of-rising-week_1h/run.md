# Backtest of 026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h

- Plan: `../../../../../03_test_plan/night4_weekend_run/plans/026-02_weekend-drop-reverses-early-week.d2_weekend-break-of-rising-week_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.012266 | -9.112 |
| w2 | 6 | -0.000162 | 0.296 |
| w3 | 0 | None | 0.0 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.006852 | -0.41 |
| w2 | 4 | -0.004121 | 1.951 |
| w3 | 2 | 0.023092 | 0.152 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.031902 | -6.485 |
| w2 | 4 | 0.007422 | 6.219 |
| w3 | 2 | 0.050864 | 7.408 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.056487 | -9.33 |
| w2 | 5 | 0.01782 | 2.659 |
| w3 | 4 | -0.017281 | -0.016 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.033982 | -3.037 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.003098 | 1.639 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.010938 | 0.376 |
| w2 | 3 | 0.014807 | 4.117 |
| w3 | 6 | -0.040111 | -0.363 |

