# Backtest of 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 554 | 0.007849 | -32.888 |
| w2 | 572 | -0.008544 | -43.495 |
| w3 | 433 | 0.002825 | 0.445 |
| w4 | 483 | 0.018585 | 15.038 |
| w5 | 443 | 0.024383 | -30.416 |
| w6 | 452 | 0.014327 | -2.037 |
| w7 | 522 | 0.01967 | -6.974 |
| w8 | 421 | -0.044893 | -22.838 |
| w9 | 450 | -0.000495 | -16.552 |
| w10 | 493 | 0.040232 | 18.585 |
| w11 | 637 | 0.051938 | 33.219 |
| w12 | 579 | -0.027409 | -29.499 |
| w13 | 608 | 0.037826 | 3.454 |
| w14 | 403 | -0.008523 | -36.031 |
| w15 | 554 | 0.011247 | 26.538 |
| w16 | 538 | 0.045767 | -40.817 |
| w17 | 512 | 0.007421 | 34.414 |
| w18 | 623 | 0.00862 | -6.268 |
| w19 | 484 | 0.022485 | 14.623 |
| w20 | 508 | -0.006734 | -35.131 |
| w21 | 526 | 0.051289 | 30.444 |
| w22 | 426 | 0.023958 | -17.591 |
| w23 | 570 | 0.043334 | 4.474 |
| w24 | 512 | -0.012605 | -49.869 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 573 | -0.009458 | -40.092 |
| w2 | 579 | -0.015174 | -42.157 |
| w3 | 487 | -0.027557 | -24.632 |
| w4 | 480 | 0.021986 | 7.732 |
| w5 | 457 | -0.016758 | -39.615 |
| w6 | 536 | 0.010796 | -13.985 |
| w7 | 616 | 0.060784 | -9.584 |
| w8 | 431 | 0.013042 | 7.379 |
| w9 | 470 | 0.00346 | -37.792 |
| w10 | 495 | 0.030456 | 9.609 |
| w11 | 696 | 0.038062 | 64.049 |
| w12 | 632 | 0.018001 | 6.817 |
| w13 | 289 | 0.037024 | 8.433 |
| w14 | 475 | -0.026158 | -16.029 |
| w15 | 526 | 0.012246 | 26.675 |
| w16 | 567 | 0.02047 | -14.844 |
| w17 | 542 | -0.007646 | 8.472 |
| w18 | 623 | -0.01239 | 27.883 |
| w19 | 539 | 0.013355 | 50.719 |
| w20 | 488 | 0.015221 | -41.659 |
| w21 | 586 | 0.05272 | 29.492 |
| w22 | 523 | -0.008823 | -39.809 |
| w23 | 588 | 0.016394 | 66.156 |
| w24 | 492 | -0.027261 | -49.79 |

