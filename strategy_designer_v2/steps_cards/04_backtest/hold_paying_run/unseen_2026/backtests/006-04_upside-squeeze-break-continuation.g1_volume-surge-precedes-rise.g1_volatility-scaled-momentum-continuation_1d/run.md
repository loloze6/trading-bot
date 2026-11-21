# Backtest of 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d

- Plan: `../../../../../03_test_plan/hold_paying_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.025142 | -14.96 |
| w2 | 25 | 0.096278 | 6.927 |
| w3 | 4 | 0.069406 | 0.199 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.041071 | -21.454 |
| w2 | 27 | 0.011821 | -4.465 |
| w3 | 9 | 0.029021 | -4.768 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.062541 | -16.239 |
| w2 | 34 | -0.023089 | -21.163 |
| w3 | 11 | 0.136637 | 20.71 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.005591 | 10.248 |
| w2 | 38 | 0.014569 | 43.652 |
| w3 | 23 | -0.102383 | -15.152 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | 0.016436 | -5.539 |
| w2 | 21 | 0.051311 | -4.132 |
| w3 | 6 | -0.061536 | -7.762 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.007267 | 0.083 |
| w2 | 29 | 0.043617 | 49.383 |
| w3 | 21 | -0.098279 | 3.845 |

