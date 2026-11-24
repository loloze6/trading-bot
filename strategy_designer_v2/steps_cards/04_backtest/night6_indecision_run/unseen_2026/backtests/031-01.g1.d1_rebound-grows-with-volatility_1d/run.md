# Backtest of 031-01.g1.d1_rebound-grows-with-volatility_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.g1.d1_rebound-grows-with-volatility_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.296208 | 18.904 |
| w2 | 5 | -0.15945 | -15.496 |
| w3 | 6 | -0.088296 | -6.518 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.280232 | 21.352 |
| w2 | 2 | -0.075327 | -4.867 |
| w3 | 7 | 0.137498 | 4.431 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.240198 | 8.933 |
| w2 | 4 | 0.035656 | 1.442 |
| w3 | 4 | 0.014806 | -1.074 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.03857 | 2.178 |
| w2 | 6 | 0.022887 | 6.745 |
| w3 | 4 | 0.240654 | 11.675 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.291658 | 16.954 |
| w2 | 2 | -0.024517 | -1.917 |
| w3 | 5 | 0.203177 | 5.449 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.140003 | 5.899 |
| w2 | 3 | -0.054089 | -1.021 |
| w3 | 4 | 0.114941 | 4.093 |

