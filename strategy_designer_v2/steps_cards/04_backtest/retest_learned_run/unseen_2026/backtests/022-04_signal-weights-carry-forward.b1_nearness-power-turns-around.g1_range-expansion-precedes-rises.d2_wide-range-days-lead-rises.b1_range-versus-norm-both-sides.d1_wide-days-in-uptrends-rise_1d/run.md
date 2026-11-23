# Backtest of 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d

- Plan: `../../../../../03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.043165 | -3.552 |
| w2 | 27 | 0.156344 | 21.667 |
| w3 | 15 | -0.035057 | 9.326 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.10139 | -20.419 |
| w2 | 17 | 0.146859 | 11.446 |
| w3 | 14 | -0.091486 | 0.572 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | -0.058316 | -8.353 |
| w2 | 23 | 0.033981 | -4.154 |
| w3 | 17 | 0.216139 | 25.428 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.10197 | -8.387 |
| w2 | 36 | -0.038395 | 6.98 |
| w3 | 24 | -0.047881 | -1.623 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.170614 | -26.015 |
| w2 | 21 | 0.129853 | 2.536 |
| w3 | 16 | -0.06397 | -8.467 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.051773 | 5.832 |
| w2 | 39 | 0.204833 | 47.498 |
| w3 | 25 | 0.025679 | 24.178 |

