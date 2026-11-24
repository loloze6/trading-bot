# Backtest of 031-01.b1.e1_strong-run-continues-three-days_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.e1_strong-run-continues-three-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.043156 | -10.427 |
| w2 | 40 | 0.198839 | 36.056 |
| w3 | 16 | -0.081767 | -14.266 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.066328 | -20.559 |
| w2 | 38 | 0.12883 | 30.293 |
| w3 | 18 | -0.106528 | -15.96 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.112035 | -22.508 |
| w2 | 33 | 0.08372 | 11.296 |
| w3 | 14 | 0.077761 | 6.631 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 44 | 0.10876 | 30.918 |
| w2 | 52 | -0.078146 | 0.271 |
| w3 | 23 | -0.049895 | -3.89 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.017564 | -3.45 |
| w2 | 32 | 0.136398 | 24.388 |
| w3 | 16 | -0.07126 | -11.747 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.089489 | -11.91 |
| w2 | 52 | 0.106042 | 69.996 |
| w3 | 30 | -0.068869 | -10.81 |

