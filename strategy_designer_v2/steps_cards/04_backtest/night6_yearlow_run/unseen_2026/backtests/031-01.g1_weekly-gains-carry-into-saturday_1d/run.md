# Backtest of 031-01.g1_weekly-gains-carry-into-saturday_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1_weekly-gains-carry-into-saturday_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.022315 | -3.591 |
| w2 | 5 | -0.028089 | -2.08 |
| w3 | 3 | 0.052443 | 0.781 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.006196 | -1.843 |
| w2 | 4 | -0.054479 | -2.89 |
| w3 | 3 | 0.066831 | 0.757 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.028662 | -4.614 |
| w2 | 5 | 0.0025 | -1.795 |
| w3 | 3 | 0.130678 | 9.963 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.004095 | -0.055 |
| w2 | 10 | -0.067804 | -4.146 |
| w3 | 4 | 0.07966 | 3.626 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.037215 | -5.385 |
| w2 | 3 | 0.050149 | 3.281 |
| w3 | 3 | -0.039078 | -1.482 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.100192 | 5.896 |
| w2 | 8 | 0.04486 | 6.03 |
| w3 | 6 | -0.093113 | -4.276 |

