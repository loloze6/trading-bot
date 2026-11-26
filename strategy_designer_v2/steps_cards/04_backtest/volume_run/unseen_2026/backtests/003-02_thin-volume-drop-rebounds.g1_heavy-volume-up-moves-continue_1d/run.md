# Backtest of 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d

- Plan: `../../../../../03_test_plan/volume_run/plans/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.082427 | -16.325 |
| w2 | 18 | 0.171733 | 22.925 |
| w3 | 12 | -0.226877 | -18.531 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.07222 | -14.959 |
| w2 | 17 | 0.11243 | 16.043 |
| w3 | 9 | -0.183353 | -18.264 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.002142 | -7.845 |
| w2 | 18 | 0.097014 | 7.921 |
| w3 | 13 | 0.017105 | 1.688 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.020424 | -10.82 |
| w2 | 30 | -0.119036 | -19.581 |
| w3 | 16 | -0.18217 | -19.294 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.0562 | 5.193 |
| w2 | 24 | 0.288696 | 39.58 |
| w3 | 13 | -0.230103 | -20.696 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.123718 | 13.611 |
| w2 | 33 | 0.065094 | 19.407 |
| w3 | 14 | 0.046766 | 5.084 |

