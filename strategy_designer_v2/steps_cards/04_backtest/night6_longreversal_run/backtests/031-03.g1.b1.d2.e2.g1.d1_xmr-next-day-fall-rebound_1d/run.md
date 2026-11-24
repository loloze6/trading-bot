# Backtest of 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XMR as XMRUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | 0.036563 | -1.166 |
| w2 | 39 | 0.051661 | 1.063 |
| w3 | 34 | 0.105048 | 0.562 |
| w4 | 41 | 0.18723 | 15.065 |
| w5 | 44 | 0.049508 | -9.463 |
| w6 | 45 | 0.158804 | 10.629 |
| w7 | 47 | 0.192497 | 10.419 |
| w8 | 37 | 0.180357 | 13.961 |
| w9 | 47 | 0.075213 | -4.273 |
| w10 | 41 | 0.300603 | 34.776 |
| w11 | 33 | 0.081422 | 16.558 |
| w12 | 42 | 0.003782 | -5.221 |
| w13 | 46 | 0.133021 | 9.723 |
| w14 | 44 | 0.096393 | -5.994 |
| w15 | 38 | -0.034341 | -3.949 |
| w16 | 42 | 0.13546 | 8.365 |
| w17 | 40 | 0.178718 | 17.448 |
| w18 | 39 | 0.350075 | 40.714 |
| w19 | 41 | 0.272219 | 28.459 |
| w20 | 35 | 0.28641 | 26.655 |
| w21 | 34 | 0.024041 | -2.169 |
| w22 | 35 | 0.101322 | 11.818 |
| w23 | 47 | -0.0627 | -8.974 |
| w24 | 30 | -0.101912 | -2.55 |

