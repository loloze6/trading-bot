# Backtest of 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.016903 | -2.861 |
| w2 | 22 | 0.109499 | 21.5 |
| w3 | 15 | 0.09195 | -1.094 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.062261 | -14.12 |
| w2 | 22 | 0.066415 | 10.792 |
| w3 | 10 | 0.132532 | -0.112 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.041912 | -17.777 |
| w2 | 22 | 0.077367 | -1.824 |
| w3 | 13 | 0.17664 | 25.83 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.089362 | 15.954 |
| w2 | 28 | 0.024477 | 27.26 |
| w3 | 19 | -0.052008 | -4.896 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.019018 | -15.305 |
| w2 | 12 | 0.068625 | -2.513 |
| w3 | 10 | -0.080677 | -8.73 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.00826 | -8.345 |
| w2 | 28 | 0.07481 | 79.265 |
| w3 | 19 | 0.133052 | 10.049 |

