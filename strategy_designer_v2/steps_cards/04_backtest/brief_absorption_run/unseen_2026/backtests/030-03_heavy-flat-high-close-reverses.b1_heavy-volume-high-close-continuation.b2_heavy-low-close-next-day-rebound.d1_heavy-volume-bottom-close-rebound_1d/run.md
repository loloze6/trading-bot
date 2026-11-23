# Backtest of 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d

- Plan: `../../../../../03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.100602 | -0.849 |
| w2 | 6 | -0.090564 | -6.033 |
| w3 | 2 | -0.119448 | -5.431 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.231375 | 8.628 |
| w2 | 2 | -0.080157 | -3.396 |
| w3 | 6 | 0.010386 | -2.266 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | -0.045715 | -3.657 |
| w2 | 7 | 0.118982 | 5.511 |
| w3 | 4 | -0.046994 | -2.035 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.002053 | -0.817 |
| w2 | 11 | 0.113012 | 13.5 |
| w3 | 2 | -0.134081 | -4.359 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.145529 | 0.673 |
| w2 | 8 | -0.024539 | -3.14 |
| w3 | 3 | 0.048743 | 2.173 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.27085 | 8.556 |
| w2 | 5 | -0.098534 | 0.581 |
| w3 | 2 | -0.09163 | -1.813 |

