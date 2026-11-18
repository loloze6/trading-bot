# Backtest of 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d

- Plan: `../../../../../03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.025142 | -9.059 |
| w2 | 26 | 0.096278 | 15.715 |
| w3 | 4 | 0.069406 | 0.199 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.041071 | -14.313 |
| w2 | 25 | 0.011821 | 2.749 |
| w3 | 7 | 0.029021 | -5.354 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.062541 | -19.115 |
| w2 | 30 | -0.023089 | -11.384 |
| w3 | 9 | 0.136637 | 20.31 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.005591 | -0.216 |
| w2 | 42 | 0.014569 | 37.344 |
| w3 | 21 | -0.102383 | -12.104 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.016436 | -4.115 |
| w2 | 21 | 0.051311 | 5.7 |
| w3 | 6 | -0.061536 | -8.863 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.007267 | -0.229 |
| w2 | 30 | 0.043617 | 47.72 |
| w3 | 19 | -0.098279 | -9.147 |

