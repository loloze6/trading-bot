# Backtest of 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 503 | 0.002222 | -34.792 |
| w2 | 427 | -0.010446 | -54.532 |
| w3 | 405 | -0.011167 | -29.117 |
| w4 | 415 | 0.039035 | 65.982 |
| w5 | 419 | 0.01487 | -28.895 |
| w6 | 458 | -0.021821 | 24.573 |
| w7 | 436 | -0.013487 | -26.26 |
| w8 | 376 | 0.024583 | 42.418 |
| w9 | 353 | 0.044606 | 14.509 |
| w10 | 416 | -0.03125 | -8.77 |
| w11 | 502 | -0.003601 | 18.361 |
| w12 | 518 | 0.014324 | -32.113 |
| w13 | 437 | 0.00209 | -31.638 |
| w14 | 356 | -0.033552 | -62.996 |
| w15 | 468 | 0.013242 | 39.329 |
| w16 | 438 | 0.012921 | -32.074 |
| w17 | 509 | -4e-05 | 25.087 |
| w18 | 466 | 0.024377 | -22.83 |
| w19 | 431 | -0.010474 | 39.527 |
| w20 | 464 | -0.025745 | -26.848 |
| w21 | 504 | 0.015017 | 32.213 |
| w22 | 366 | -0.009548 | -25.848 |
| w23 | 564 | -0.031297 | -13.725 |
| w24 | 446 | 0.003391 | -28.699 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 488 | -0.026311 | -42.716 |
| w2 | 432 | 0.016216 | -42.944 |
| w3 | 388 | 0.023337 | -30.248 |
| w4 | 441 | 0.017343 | 32.048 |
| w5 | 432 | -0.011654 | -32.169 |
| w6 | 482 | -0.009884 | -28.103 |
| w7 | 477 | -0.010005 | -33.405 |
| w8 | 348 | -0.003243 | 25.271 |
| w9 | 408 | 0.004758 | -16.502 |
| w10 | 454 | -0.002135 | 55.733 |
| w11 | 518 | 0.014498 | 61.094 |
| w12 | 490 | 0.009363 | 17.497 |
| w13 | 258 | 0.007029 | 8.09 |
| w14 | 369 | -0.004536 | -45.473 |
| w15 | 431 | -0.024884 | 6.998 |
| w16 | 441 | -0.00464 | 35.433 |
| w17 | 487 | 0.008377 | -20.384 |
| w18 | 495 | 0.054834 | 25.413 |
| w19 | 448 | -0.010583 | 48.319 |
| w20 | 412 | -0.009329 | -0.477 |
| w21 | 523 | -0.024843 | 15.286 |
| w22 | 376 | 0.036392 | -31.319 |
| w23 | 519 | 0.017522 | 68.292 |
| w24 | 415 | 0.007838 | -34.448 |

