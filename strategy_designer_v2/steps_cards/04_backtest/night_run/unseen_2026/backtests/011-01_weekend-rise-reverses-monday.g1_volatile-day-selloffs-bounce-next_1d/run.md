# Backtest of 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d

- Plan: `../../../../../03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.011627 | -15.874 |
| w2 | 33 | -0.17043 | -23.589 |
| w3 | 23 | -0.114988 | -18.048 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.084482 | -24.523 |
| w2 | 34 | -0.172633 | -23.881 |
| w3 | 21 | -0.022663 | -11.11 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.128596 | 7.609 |
| w2 | 32 | -0.126308 | -29.824 |
| w3 | 14 | 0.104038 | 4.144 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.079261 | 8.06 |
| w2 | 20 | 0.123538 | 30.183 |
| w3 | 19 | -0.165334 | -19.731 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.01279 | -17.637 |
| w2 | 40 | -0.124298 | -26.181 |
| w3 | 20 | 0.048128 | -3.226 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.023514 | -6.407 |
| w2 | 18 | -0.040396 | 0.615 |
| w3 | 20 | 0.098813 | 7.09 |

