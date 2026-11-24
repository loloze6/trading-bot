# Backtest of 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h

- Plan: `../../../../../03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.033523 | 2.801 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.037797 | 0.606 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.02879 | 1.964 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.04837 | 0.453 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.03249 | -2.202 |
| w2 | 8 | -0.014928 | -8.139 |
| w3 | 5 | 0.041193 | 2.768 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.043267 | 12.181 |
| w2 | 8 | 0.00984 | 16.032 |
| w3 | 4 | 0.014066 | -2.08 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -3.1e-05 | 10.495 |
| w2 | 4 | -0.030626 | -5.522 |
| w3 | 2 | 0.037206 | -0.603 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.046832 | 4.475 |
| w2 | 4 | -0.02147 | -2.554 |
| w3 | 3 | -0.027039 | -1.565 |

