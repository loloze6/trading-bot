# Backtest of 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.054904 | -14.119 |
| w2 | 22 | 0.095414 | 19.024 |
| w3 | 12 | 0.056152 | -3.74 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.065295 | -19.593 |
| w2 | 20 | 0.043928 | 6.656 |
| w3 | 9 | 0.08162 | -0.462 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.038622 | -5.037 |
| w2 | 25 | -0.088224 | -17.39 |
| w3 | 15 | 0.168647 | 28.569 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.051786 | -6.99 |
| w2 | 31 | 0.055748 | 33.621 |
| w3 | 28 | -0.028945 | -6.192 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | -0.145172 | -23.874 |
| w2 | 14 | 0.055048 | 3.178 |
| w3 | 8 | 0.004826 | -7.192 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.061208 | 8.399 |
| w2 | 27 | 0.05789 | 59.318 |
| w3 | 8 | 0.20759 | 44.871 |

