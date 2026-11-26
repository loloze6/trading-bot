# Backtest of 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d

- Plan: `../../../../../03_test_plan/night_013_run/plans/013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.078957 | 6.303 |
| w2 | 17 | 0.207032 | 23.595 |
| w3 | 20 | -0.01922 | 1.922 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.080085 | 4.222 |
| w2 | 15 | 0.142603 | 16.448 |
| w3 | 20 | -0.007726 | 4.36 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.003796 | 0.029 |
| w2 | 20 | 0.126835 | 13.325 |
| w3 | 17 | 0.08907 | 6.065 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.206178 | 19.98 |
| w2 | 25 | 0.010545 | 6.005 |
| w3 | 23 | -0.188124 | -11.022 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | 0.038965 | 0.172 |
| w2 | 17 | 0.178665 | 12.721 |
| w3 | 14 | -0.231761 | -6.787 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.020875 | -5.097 |
| w2 | 29 | 0.072021 | 15.388 |
| w3 | 27 | -0.008443 | -1.835 |

