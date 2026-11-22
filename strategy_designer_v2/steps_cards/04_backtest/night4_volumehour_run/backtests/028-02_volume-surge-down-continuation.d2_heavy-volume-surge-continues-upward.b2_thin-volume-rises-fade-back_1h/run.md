# Backtest of 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b2_thin-volume-rises-fade-back_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 429 | 0.010997 | -4.532 |
| w2 | 359 | -0.04823 | -27.899 |
| w3 | 356 | -0.00438 | 16.45 |
| w4 | 354 | 0.033035 | -18.607 |
| w5 | 397 | 0.027867 | -12.67 |
| w6 | 423 | 0.007259 | -30.572 |
| w7 | 347 | 0.036729 | 2.218 |
| w8 | 423 | 0.008131 | -17.742 |
| w9 | 339 | 0.040079 | 11.952 |
| w10 | 434 | -0.01253 | -26.829 |
| w11 | 503 | -0.021757 | -21.089 |
| w12 | 426 | -0.018237 | -10.291 |
| w13 | 313 | 0.022239 | 2.658 |
| w14 | 342 | 0.007987 | 4.593 |
| w15 | 355 | -0.025584 | -19.222 |
| w16 | 358 | -0.003173 | -13.126 |
| w17 | 422 | 0.019476 | -25.632 |
| w18 | 458 | -0.008051 | -13.848 |
| w19 | 409 | -0.024463 | -32.575 |
| w20 | 398 | 0.002896 | -11.968 |
| w21 | 433 | 0.031395 | -6.653 |
| w22 | 377 | -0.010642 | -8.063 |
| w23 | 467 | -0.013379 | -28.392 |
| w24 | 411 | -0.004821 | -14.791 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 473 | 0.006241 | -15.021 |
| w2 | 398 | -0.032163 | -9.27 |
| w3 | 458 | -0.00974 | -11.701 |
| w4 | 422 | -0.02303 | -24.058 |
| w5 | 458 | -0.016624 | -17.892 |
| w6 | 455 | -0.031385 | -27.325 |
| w7 | 406 | 0.011061 | -5.607 |
| w8 | 352 | 0.015775 | -16.622 |
| w9 | 416 | 0.010794 | 1.768 |
| w10 | 462 | -0.007316 | -27.173 |
| w11 | 449 | -0.01983 | -25.619 |
| w12 | 458 | -0.00909 | -12.373 |
| w13 | 146 | 0.028623 | -11.522 |
| w14 | 286 | 0.010982 | -4.126 |
| w15 | 377 | 0.026393 | 10.09 |
| w16 | 414 | -0.01801 | -19.545 |
| w17 | 435 | 0.024823 | -14.262 |
| w18 | 461 | 0.005963 | -12.877 |
| w19 | 465 | -0.008741 | -36.626 |
| w20 | 382 | 0.032224 | 0.307 |
| w21 | 464 | 0.033115 | -3.37 |
| w22 | 390 | 0.038965 | 37.273 |
| w23 | 473 | -0.009796 | -21.775 |
| w24 | 431 | 0.027504 | 7.751 |

