# Backtest of 031-01.g1.d2_wide-low-close-in-volatile-coins_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.g1.d2_wide-low-close-in-volatile-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.274086 | 17.104 |
| w2 | 3 | -0.076413 | -6.983 |
| w3 | 4 | -0.102138 | -9.602 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.25201 | 23.044 |
| w2 | 1 | -0.030986 | -1.389 |
| w3 | 2 | 0.139759 | 5.361 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.288004 | 10.92 |
| w2 | 3 | 0.043987 | 2.585 |
| w3 | 2 | 0.019416 | -0.763 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.028649 | 0.44 |
| w2 | 4 | 0.010003 | 4.777 |
| w3 | 2 | 0.279884 | 15.64 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.285622 | 18.766 |
| w2 | 1 | -0.027478 | -1.842 |
| w3 | 3 | 0.223979 | 11.801 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.07382 | -3.051 |
| w2 | 3 | -0.032781 | 0.179 |
| w3 | 1 | 0.129922 | 4.619 |

