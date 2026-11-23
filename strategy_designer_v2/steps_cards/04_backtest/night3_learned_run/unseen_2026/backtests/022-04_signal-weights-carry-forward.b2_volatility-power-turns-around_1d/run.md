# Backtest of 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | 0.024049 | 2.507 |
| w2 | 23 | 0.104704 | 18.951 |
| w3 | 13 | -0.157754 | -15.826 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.065067 | 3.135 |
| w2 | 27 | 0.041443 | 12.561 |
| w3 | 25 | -0.06476 | -18.242 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | 0.108052 | 42.225 |
| w2 | 24 | 0.145579 | 46.785 |
| w3 | 16 | -0.077573 | -3.505 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.125106 | -40.054 |
| w2 | 32 | -0.080404 | -51.098 |
| w3 | 16 | 0.025818 | -5.175 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.020366 | -15.651 |
| w2 | 22 | 0.095965 | 31.715 |
| w3 | 15 | 0.156565 | 20.785 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.048674 | 3.035 |
| w2 | 18 | 0.083811 | 35.68 |
| w3 | 20 | 0.13149 | 16.966 |

