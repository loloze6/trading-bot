# Backtest of 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d

- Plan: `../../../../../03_test_plan/night6_streak_run/plans/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | -0.087916 | -35.543 |
| w2 | 15 | -0.066238 | 2.702 |
| w3 | 18 | -0.122841 | -23.141 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.177021 | -39.356 |
| w2 | 13 | 0.076879 | 20.556 |
| w3 | 11 | -0.090734 | -19.133 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.011569 | -18.589 |
| w2 | 18 | -0.076174 | -24.049 |
| w3 | 9 | 0.095771 | 3.123 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.107903 | 7.882 |
| w2 | 15 | 0.089979 | 15.019 |
| w3 | 26 | 0.01653 | -13.587 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.200843 | -7.352 |
| w2 | 30 | -0.132455 | -31.054 |
| w3 | 10 | 0.024218 | -1.033 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.091836 | -11.325 |
| w2 | 23 | -0.043572 | -0.247 |
| w3 | 16 | 0.249724 | 18.472 |

