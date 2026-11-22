# Backtest of 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d

- Plan: `../../../../03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.007112 | 0.0 |
| w2 | 2 | -0.016302 | 2.863 |
| w3 | 4 | 0.039309 | 5.118 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.006741 | 0.736 |
| w9 | 2 | 0.048663 | -0.255 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.005138 | 0.063 |
| w14 | 5 | 0.008681 | 3.258 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.03729 | -5.81 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.290044 | 5.384 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.114841 | 0.779 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.000333 | -0.297 |
| w2 | 2 | -0.00602 | -3.58 |
| w3 | 2 | 0.029112 | 1.618 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.059237 | 4.996 |
| w6 | 2 | -0.023237 | -0.228 |
| w7 | 1 | 0.134074 | 11.883 |
| w8 | 2 | 0.006012 | -0.687 |
| w9 | 1 | 0.085567 | 3.649 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.001303 | -0.471 |
| w14 | 8 | -0.069174 | -4.792 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.080179 | -0.196 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.353538 | 9.118 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.080225 | 0.0 |
| w2 | 3 | 0.152964 | 14.5 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.147513 | 5.95 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.058729 | 0.237 |
| w10 | 2 | 0.053883 | -1.402 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | 0.143956 | 4.304 |
| w14 | 4 | -0.021669 | 0.076 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | 0.091506 | -0.474 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.030672 | -4.624 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.02204 | -0.928 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.055648 | -0.424 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.011594 | 15.393 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.035741 | -4.779 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.114512 | 1.238 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | None | -0.032 |
| w8 | 2 | -0.014031 | -0.568 |
| w9 | 4 | 0.033337 | 4.624 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.054704 | 0.179 |
| w13 | 2 | 0.020819 | -0.426 |
| w14 | 4 | 0.058131 | 3.236 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.016986 | -8.09 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.007367 | -4.506 |
| w19 | 1 | 0.03075 | 0.423 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.09254 | -7.49 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.308005 | -7.701 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | -0.005085 | 4.81 |
| w4 | 2 | -0.005484 | -0.93 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 3 | 0.07387 | 4.752 |
| w8 | 3 | 0.060872 | 0.462 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.079339 | -5.508 |
| w11 | 0 | 0.031804 | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | 0.10587 | -2.192 |
| w14 | 2 | -0.032431 | -8.296 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | 0.071014 | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.04838 | -8.689 |
| w19 | 2 | -0.011558 | -0.036 |
| w20 | 1 | 0.177847 | -0.138 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.028083 | -0.658 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.082525 | 6.195 |
| w4 | 2 | -0.060514 | -7.775 |
| w5 | 2 | 0.03744 | 22.086 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.02647 | 0.0 |
| w8 | 2 | -0.010962 | -4.5 |
| w9 | 2 | 0.070873 | 0.411 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.06634 | -0.544 |
| w14 | 2 | 0.092181 | 3.085 |
| w15 | 1 | 0.099848 | 13.01 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.021306 | -4.6 |
| w19 | 2 | -0.199592 | -4.943 |
| w20 | 3 | 0.130247 | -14.381 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.164207 | -0.179 |
| w23 | 3 | -0.1319 | 0.878 |
| w24 | 0 | None | 0.0 |

