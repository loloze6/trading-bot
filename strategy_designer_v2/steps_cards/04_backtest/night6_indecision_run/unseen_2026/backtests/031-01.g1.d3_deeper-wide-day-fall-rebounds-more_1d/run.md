# Backtest of 031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.g1.d3_deeper-wide-day-fall-rebounds-more_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.249089 | 19.682 |
| w2 | 5 | -0.220924 | -20.582 |
| w3 | 6 | -0.104765 | -11.805 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.257591 | 22.73 |
| w2 | 2 | -0.079716 | -5.726 |
| w3 | 7 | 0.095804 | 3.258 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.218645 | 9.751 |
| w2 | 5 | 0.069445 | 4.377 |
| w3 | 3 | 0.121199 | 6.367 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.073899 | 8.245 |
| w2 | 6 | 0.050859 | 12.47 |
| w3 | 4 | 0.193922 | 9.603 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.204976 | 11.29 |
| w2 | 2 | -0.015196 | -1.741 |
| w3 | 5 | 0.174647 | 9.955 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.136125 | 7.07 |
| w2 | 3 | -0.04137 | -0.36 |
| w3 | 4 | 0.049092 | 2.172 |

