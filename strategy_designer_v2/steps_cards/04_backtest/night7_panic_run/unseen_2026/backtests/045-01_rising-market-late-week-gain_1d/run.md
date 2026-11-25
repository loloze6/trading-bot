# Backtest of 045-01_rising-market-late-week-gain_1d

- Plan: `../../../../../03_test_plan/night7_panic_run/plans/045-01_rising-market-late-week-gain_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.032929 | -1.59 |
| w2 | 9 | -0.036484 | -3.847 |
| w3 | 10 | 0.109788 | 4.481 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.002667 | -0.268 |
| w2 | 5 | 0.042121 | 3.905 |
| w3 | 10 | 0.173748 | 6.993 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.019916 | -0.472 |
| w2 | 3 | -0.07006 | -3.819 |
| w3 | 11 | 0.16046 | 19.002 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.135418 | -10.389 |
| w2 | 9 | -0.100251 | -4.224 |
| w3 | 13 | 0.222886 | 24.49 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 4 | 0.029668 | 2.395 |
| w3 | 10 | 0.079377 | 1.168 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.028845 | 1.181 |
| w2 | 14 | 0.036668 | 23.448 |
| w3 | 10 | 0.057178 | 8.453 |

