# Backtest of 031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.020113 | 0.135 |
| w2 | 8 | 0.038543 | 2.588 |
| w3 | 3 | 0.030511 | 0.243 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.054382 | 3.346 |
| w2 | 7 | -0.029589 | -2.178 |
| w3 | 2 | 0.072118 | 0.459 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.02099 | -5.162 |
| w2 | 5 | 0.069746 | 3.886 |
| w3 | 3 | 0.17701 | 13.052 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | -0.026703 | -2.995 |
| w2 | 9 | -0.073774 | -5.808 |
| w3 | 3 | 0.049062 | 0.939 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.009903 | -4.767 |
| w2 | 5 | 0.040442 | 2.766 |
| w3 | 2 | 0.048145 | 0.847 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.025228 | 1.001 |
| w2 | 7 | 0.075131 | 9.944 |
| w3 | 6 | -0.09296 | -5.323 |

