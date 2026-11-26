# Backtest of 031-03.b1_wide-day-extends-up-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-03.b1_wide-day-extends-up-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.081085 | -6.474 |
| w2 | 6 | 0.195303 | 34.108 |
| w3 | 9 | -0.173151 | -7.588 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.096018 | -16.691 |
| w2 | 6 | 0.157161 | 8.304 |
| w3 | 7 | -0.241944 | -14.098 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.084344 | -2.522 |
| w2 | 9 | 0.062906 | 7.458 |
| w3 | 7 | 0.161996 | 24.082 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.046969 | 5.768 |
| w2 | 14 | -0.115031 | 2.845 |
| w3 | 12 | -0.083124 | 6.766 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.131647 | -12.334 |
| w2 | 10 | 0.282545 | 23.569 |
| w3 | 7 | -0.008672 | -5.672 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.004802 | -7.246 |
| w2 | 15 | 0.130895 | 39.689 |
| w3 | 7 | 0.054652 | 20.082 |

