# Backtest of 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h

- Plan: `../../../../../03_test_plan/night4_weekend_run/plans/026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.010791 | -4.872 |
| w2 | 20 | -0.025603 | -12.32 |
| w3 | 14 | 0.003274 | -5.322 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.013206 | -8.147 |
| w2 | 27 | -0.017018 | -7.018 |
| w3 | 16 | -0.002501 | -0.747 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.005014 | -6.975 |
| w2 | 19 | -0.014998 | -14.194 |
| w3 | 0 | None | 0.0 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.036933 | 1.486 |
| w2 | 23 | 0.011936 | 16.454 |
| w3 | 14 | 0.008554 | 6.513 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.004086 | -1.459 |
| w2 | 20 | -0.021152 | -6.679 |
| w3 | 4 | 0.013993 | 2.169 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.006002 | -1.778 |
| w2 | 22 | 0.012453 | -0.769 |
| w3 | 15 | -0.027037 | 4.333 |

