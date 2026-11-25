# Backtest of 045-01_agitated-wide-low-close-rebound_1d

- Plan: `../../../../../03_test_plan/night7_chopreversal_run/plans/045-01_agitated-wide-low-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 70 | 0.027736 | -16.946 |
| w2 | 35 | -0.05319 | -9.607 |
| w3 | 26 | 0.075809 | -0.43 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.067493 | -16.736 |
| w2 | 22 | -0.025056 | -2.725 |
| w3 | 18 | 0.159575 | 7.171 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | 0.129794 | 5.66 |
| w2 | 0 | None | 0.0 |
| w3 | 53 | 0.073368 | 2.261 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 37 | -0.100699 | -17.056 |
| w2 | 31 | -0.104583 | -7.663 |
| w3 | 12 | 0.072459 | 4.287 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.205216 | 16.78 |
| w2 | 11 | 0.194781 | 20.283 |
| w3 | 39 | 0.084847 | -1.76 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 84 | -0.128238 | -24.748 |
| w2 | 39 | -0.101657 | -2.763 |
| w3 | 26 | 0.117858 | 14.05 |

