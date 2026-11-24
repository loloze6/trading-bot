# Backtest of 035-01_falling-agitated-scaled-fall-rebound_1d

- Plan: `../../../../../03_test_plan/night7_chopreversal_run/plans/035-01_falling-agitated-scaled-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | -0.09268 | -25.869 |
| w2 | 14 | -0.03567 | -3.841 |
| w3 | 2 | 0.114969 | 3.268 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | -0.049203 | -11.963 |
| w2 | 6 | -0.069569 | -4.596 |
| w3 | 2 | 0.182444 | 5.469 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.159931 | 6.816 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.099772 | 3.234 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.163414 | 8.23 |
| w2 | 9 | 0.046606 | 1.613 |
| w3 | 0 | None | 0.0 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | 0.37097 | 20.243 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | 0.124397 | 5.834 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | -0.120443 | -19.113 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |

