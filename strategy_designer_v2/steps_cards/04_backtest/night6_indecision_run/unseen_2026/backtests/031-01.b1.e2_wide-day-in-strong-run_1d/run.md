# Backtest of 031-01.b1.e2_wide-day-in-strong-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.e2_wide-day-in-strong-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.087959 | -7.16 |
| w2 | 31 | 0.247661 | 28.6 |
| w3 | 15 | -0.136973 | -7.791 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.136628 | -16.34 |
| w2 | 28 | 0.15071 | 15.796 |
| w3 | 15 | -0.203018 | -14.23 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.093747 | -7.987 |
| w2 | 24 | 0.098267 | 6.258 |
| w3 | 15 | 0.08939 | 7.053 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.043488 | 7.824 |
| w2 | 45 | -0.139506 | -6.688 |
| w3 | 18 | -0.107395 | 5.845 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.059326 | -7.184 |
| w2 | 27 | 0.282132 | 27.605 |
| w3 | 12 | -0.220195 | -14.898 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.007605 | -7.294 |
| w2 | 34 | 0.21148 | 73.524 |
| w3 | 17 | 0.093613 | 14.092 |

