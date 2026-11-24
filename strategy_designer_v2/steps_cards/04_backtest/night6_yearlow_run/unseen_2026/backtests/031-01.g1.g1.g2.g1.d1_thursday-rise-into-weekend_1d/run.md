# Backtest of 031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d1_thursday-rise-into-weekend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.04172 | -0.682 |
| w2 | 13 | 0.085948 | 1.431 |
| w3 | 6 | -0.070384 | -3.244 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.058374 | 1.272 |
| w2 | 8 | 0.101545 | 3.465 |
| w3 | 4 | -0.047448 | -0.918 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.055661 | -2.4 |
| w2 | 10 | 0.158136 | 4.684 |
| w3 | 8 | 0.131215 | 19.638 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.142976 | -15.95 |
| w2 | 15 | 0.014771 | 15.887 |
| w3 | 9 | -0.067147 | 14.467 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.039391 | -3.968 |
| w2 | 7 | 0.124886 | 6.015 |
| w3 | 4 | -0.019835 | -2.506 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.051509 | -4.392 |
| w2 | 14 | 0.07481 | 27.863 |
| w3 | 10 | 0.188714 | 7.334 |

