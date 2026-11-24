# Backtest of 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | -0.021231 | -5.471 |
| w2 | 15 | 0.244397 | 33.091 |
| w3 | 18 | -0.045573 | -11.574 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.059286 | -13.502 |
| w2 | 13 | 0.134307 | 18.807 |
| w3 | 12 | 0.029202 | -2.631 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.08787 | -9.172 |
| w2 | 9 | 0.111656 | 14.109 |
| w3 | 12 | 0.082777 | 9.092 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.118544 | 23.393 |
| w2 | 39 | -0.10443 | -2.301 |
| w3 | 25 | -0.092662 | -8.791 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.039388 | -9.562 |
| w2 | 9 | 0.099622 | 7.726 |
| w3 | 13 | 0.087691 | 0.242 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.054217 | 4.447 |
| w2 | 41 | 0.08624 | 58.302 |
| w3 | 22 | 0.03719 | 1.622 |

