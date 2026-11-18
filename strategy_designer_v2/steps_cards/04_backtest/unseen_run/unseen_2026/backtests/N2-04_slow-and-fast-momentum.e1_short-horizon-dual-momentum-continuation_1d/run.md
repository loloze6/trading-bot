# Backtest of N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d

- Plan: `../../../../../03_test_plan/validation_run/plans/N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.009084 | -7.167 |
| w2 | 18 | 0.139165 | 24.487 |
| w3 | 10 | 0.075136 | -0.481 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.060355 | -10.136 |
| w2 | 9 | 0.09403 | 15.729 |
| w3 | 10 | 0.073431 | -3.037 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.001719 | -2.215 |
| w2 | 16 | -0.005518 | -2.901 |
| w3 | 9 | 0.154675 | 25.379 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.036782 | -6.197 |
| w2 | 20 | 0.115053 | 61.581 |
| w3 | 23 | 0.010865 | 1.449 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.021522 | -2.199 |
| w2 | 8 | 0.030778 | 5.421 |
| w3 | 8 | 0.024154 | -3.256 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.023532 | 1.415 |
| w2 | 19 | 0.088259 | 54.885 |
| w3 | 15 | 0.183159 | 34.716 |

