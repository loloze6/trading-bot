# Backtest of 033-03.b2_rising-market-range-top-continuation_1d

- Plan: `../../../../../03_test_plan/night7_rangefail_run/plans/033-03.b2_rising-market-range-top-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.020262 | 3.662 |
| w2 | 18 | 0.120037 | 18.913 |
| w3 | 25 | -0.049125 | -7.373 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.037407 | -1.88 |
| w2 | 18 | 0.176607 | 39.611 |
| w3 | 20 | -0.00242 | 3.049 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.019916 | -3.953 |
| w2 | 11 | -0.169498 | -18.541 |
| w3 | 34 | 0.13485 | 35.679 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.109047 | -15.12 |
| w2 | 35 | 0.030924 | 39.456 |
| w3 | 43 | 0.031727 | 6.346 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 3 | 0.128032 | 11.973 |
| w3 | 27 | -0.089382 | -2.22 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.138328 | 10.755 |
| w2 | 46 | 0.072942 | 77.312 |
| w3 | 36 | 0.012627 | 2.579 |

