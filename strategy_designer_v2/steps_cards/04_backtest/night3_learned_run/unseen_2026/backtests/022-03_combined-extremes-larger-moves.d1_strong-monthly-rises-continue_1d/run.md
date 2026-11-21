# Backtest of 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.054904 | -12.837 |
| w2 | 27 | 0.095414 | 15.816 |
| w3 | 13 | 0.056152 | -4.8 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.065295 | -15.469 |
| w2 | 26 | 0.043928 | 7.335 |
| w3 | 11 | 0.08162 | -0.797 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.038622 | -5.852 |
| w2 | 30 | -0.088224 | -16.482 |
| w3 | 15 | 0.168647 | 28.569 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.051786 | -5.412 |
| w2 | 37 | 0.055748 | 47.741 |
| w3 | 30 | -0.028945 | -3.346 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.145172 | -21.949 |
| w2 | 16 | 0.055048 | 7.607 |
| w3 | 9 | 0.004826 | -7.027 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.061208 | 9.362 |
| w2 | 35 | 0.05789 | 54.181 |
| w3 | 8 | 0.20759 | 44.86 |

