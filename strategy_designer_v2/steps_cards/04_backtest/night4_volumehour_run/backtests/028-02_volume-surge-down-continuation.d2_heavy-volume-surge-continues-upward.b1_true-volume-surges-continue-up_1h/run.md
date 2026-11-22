# Backtest of 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward.b1_true-volume-surges-continue-up_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 567 | 0.002222 | -39.061 |
| w2 | 490 | -0.010446 | -41.526 |
| w3 | 484 | -0.011167 | -36.232 |
| w4 | 492 | 0.039035 | 53.165 |
| w5 | 481 | 0.01487 | -27.487 |
| w6 | 538 | -0.021821 | -15.313 |
| w7 | 504 | -0.013487 | -22.395 |
| w8 | 417 | 0.024583 | 48.37 |
| w9 | 388 | 0.044606 | 14.451 |
| w10 | 500 | -0.03125 | -11.793 |
| w11 | 633 | -0.003601 | -0.132 |
| w12 | 575 | 0.014324 | -24.577 |
| w13 | 548 | 0.00209 | -35.975 |
| w14 | 407 | -0.033552 | -63.794 |
| w15 | 540 | 0.013242 | 25.896 |
| w16 | 526 | 0.012921 | -28.755 |
| w17 | 647 | -4e-05 | 0.044 |
| w18 | 559 | 0.024377 | -19.135 |
| w19 | 535 | -0.010474 | 20.275 |
| w20 | 537 | -0.025745 | -29.981 |
| w21 | 583 | 0.015017 | 8.411 |
| w22 | 463 | -0.009548 | -34.599 |
| w23 | 684 | -0.031297 | -18.551 |
| w24 | 503 | 0.003391 | -34.937 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 583 | -0.026311 | -45.19 |
| w2 | 490 | 0.016216 | -32.523 |
| w3 | 439 | 0.023337 | -35.906 |
| w4 | 498 | 0.017343 | 32.491 |
| w5 | 454 | -0.011654 | -30.922 |
| w6 | 549 | -0.009884 | -33.986 |
| w7 | 568 | -0.010005 | -19.93 |
| w8 | 395 | -0.003243 | 23.563 |
| w9 | 428 | 0.004758 | -12.74 |
| w10 | 527 | -0.002135 | 28.558 |
| w11 | 635 | 0.014498 | 32.23 |
| w12 | 586 | 0.009363 | 5.434 |
| w13 | 304 | 0.007029 | -6.846 |
| w14 | 443 | -0.004536 | -43.059 |
| w15 | 497 | -0.024884 | -8.727 |
| w16 | 546 | -0.00464 | 5.345 |
| w17 | 617 | 0.008377 | -29.155 |
| w18 | 580 | 0.054834 | 11.1 |
| w19 | 552 | -0.010583 | 17.788 |
| w20 | 484 | -0.009329 | -1.847 |
| w21 | 618 | -0.024843 | -11.618 |
| w22 | 456 | 0.036392 | -17.906 |
| w23 | 625 | 0.017522 | 29.427 |
| w24 | 496 | 0.007838 | -31.762 |

