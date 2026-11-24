# Backtest of 031-01_wide-flat-day-ends-uprun_1d

- Plan: `../../../../03_test_plan/night6_indecision_run/plans/031-01_wide-flat-day-ends-uprun_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.07464 | 7.481 |
| w4 | 4 | -0.023744 | -14.408 |
| w5 | 2 | -0.019975 | -0.22 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.086126 | -0.127 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.008273 | -3.222 |
| w17 | 4 | -0.038246 | -10.522 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | 0.079318 | 0.871 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.060417 | -0.423 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.060934 | -9.724 |
| w8 | 2 | -0.115786 | -0.301 |
| w9 | 2 | -0.056854 | -1.005 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.030338 | -5.505 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.292994 | 26.04 |
| w15 | 0 | None | 0.0 |
| w16 | 9 | -0.028571 | -16.829 |
| w17 | 2 | 0.041214 | -20.238 |
| w18 | 2 | -0.074844 | 4.674 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.14665 | -0.102 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.118538 | 3.572 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.092633 | 0.191 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.062461 | -1.306 |
| w9 | 2 | -0.135319 | -2.384 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.026058 | -1.037 |
| w12 | 2 | -0.016057 | -0.886 |
| w13 | 1 | 0.019202 | 1.55 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.050407 | 1.928 |
| w16 | 4 | 0.010479 | -0.456 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.150209 | -24.683 |
| w20 | 1 | 0.012447 | 1.817 |
| w21 | 2 | 0.006307 | 11.148 |
| w22 | 0 | None | 0.0 |
| w23 | 4 | -0.201614 | -16.846 |
| w24 | 2 | -0.005353 | 1.524 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.051566 | -7.25 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.076137 | 5.596 |
| w10 | 4 | -0.122321 | -19.288 |
| w11 | 4 | -0.003786 | -11.2 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.063726 | 1.959 |
| w22 | 3 | 0.075392 | 14.428 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.156552 | -12.643 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | 0.0018 | -6.341 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.028281 | -6.406 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.070633 | 5.572 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.22848 | -3.506 |
| w11 | 3 | 0.012136 | 0.547 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.002069 | 3.213 |
| w14 | 3 | -0.067883 | -9.106 |
| w15 | 1 | 0.24341 | 7.935 |
| w16 | 2 | 0.034831 | 0.197 |
| w17 | 2 | -0.010323 | 15.181 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.058951 | 3.931 |
| w20 | 2 | -0.032395 | -0.076 |
| w21 | 2 | 0.059822 | -2.155 |
| w22 | 2 | -0.088792 | -7.638 |
| w23 | 2 | -0.08488 | -23.988 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.059444 | -6.887 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.052003 | 5.53 |
| w8 | 2 | 0.088587 | -5.107 |
| w9 | 2 | -0.095295 | 0.123 |
| w10 | 1 | 0.059054 | 8.019 |
| w11 | 6 | -0.098246 | -15.066 |
| w12 | 1 | 0.0295 | 4.402 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.074987 | 5.418 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.071989 | 2.556 |
| w18 | 1 | 0.036466 | 2.411 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.047399 | 0.308 |
| w21 | 2 | 0.010567 | 1.863 |
| w22 | 2 | -0.051494 | -0.541 |
| w23 | 2 | 0.18648 | 13.124 |
| w24 | 4 | -0.216166 | -9.824 |

