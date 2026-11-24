# Backtest of 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d

- Plan: `../../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XMR as XMRUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | 0.127914 | 11.339 |
| w2 | 32 | 0.162933 | 25.474 |
| w3 | 27 | -0.013494 | -4.486 |

