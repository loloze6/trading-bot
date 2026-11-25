# Backtest of 043-01_falling-agitated-intraday-drop-rebound_1d

- Plan: `../../../../../03_test_plan/night7_chopreversal_run/plans/043-01_falling-agitated-intraday-drop-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.049782 | -25.68 |
| w2 | 11 | -0.044696 | -6.6 |
| w3 | 2 | 0.110976 | 3.291 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.073388 | -20.668 |
| w2 | 6 | -0.059973 | -7.03 |
| w3 | 2 | 0.178331 | 5.507 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.075806 | 2.429 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.102589 | 4.041 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.156352 | 11.247 |
| w2 | 11 | 0.060722 | 5.156 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.179548 | 17.097 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.138215 | 7.097 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 42 | -0.146447 | -27.142 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

