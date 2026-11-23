# Backtest of 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d

- Plan: `../../../../../03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.187518 | -44.421 |
| w2 | 25 | 0.097158 | 14.914 |
| w3 | 23 | -0.135402 | -19.927 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.207935 | -35.862 |
| w2 | 25 | -0.001626 | -3.544 |
| w3 | 20 | 0.0128 | -9.404 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.147636 | -23.409 |
| w2 | 26 | 0.058643 | 2.872 |
| w3 | 10 | 0.120859 | 8.849 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.076605 | -13.219 |
| w2 | 28 | -0.086242 | -3.664 |
| w3 | 24 | 0.042941 | 5.002 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.033046 | -18.501 |
| w2 | 33 | -0.007967 | -10.247 |
| w3 | 15 | 0.004578 | -5.807 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.047289 | -7.63 |
| w2 | 26 | -0.083859 | 2.056 |
| w3 | 21 | -0.054147 | -1.744 |

