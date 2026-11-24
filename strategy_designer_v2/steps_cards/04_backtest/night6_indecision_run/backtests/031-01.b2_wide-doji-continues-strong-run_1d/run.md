# Backtest of 031-01.b2_wide-doji-continues-strong-run_1d

- Plan: `../../../../03_test_plan/night6_indecision_run/plans/031-01.b2_wide-doji-continues-strong-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.07464 | -3.689 |
| w4 | 4 | -0.048417 | 15.471 |
| w5 | 0 | 0.019975 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.086126 | 3.555 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | -0.008273 | 2.885 |
| w17 | 3 | 0.023737 | 15.914 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.053342 | -4.784 |
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
| w4 | 0 | 0.060417 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.060934 | 0.0 |
| w8 | 2 | 0.115786 | 5.544 |
| w9 | 2 | 0.056854 | 1.428 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | 0.02178 | -5.797 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | -0.292994 | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 7 | 0.038103 | 7.914 |
| w17 | 0 | -0.041214 | 0.0 |
| w18 | 2 | 0.074844 | -2.872 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.14665 | 1.704 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.118538 | -1.83 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.093124 | -1.626 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.062461 | 4.951 |
| w9 | 2 | 0.135319 | 1.562 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.014017 | 9.935 |
| w12 | 2 | 0.016057 | -0.88 |
| w13 | 1 | -0.019202 | -0.313 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.050407 | -3.388 |
| w16 | 4 | -0.017091 | 3.985 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.150209 | 42.471 |
| w20 | 1 | -0.012447 | -0.281 |
| w21 | 2 | -0.006307 | -0.651 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.16746 | 20.631 |
| w24 | 2 | 0.005353 | -2.341 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | 0.051566 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | -0.076137 | -1.403 |
| w10 | 3 | 0.100222 | 7.916 |
| w11 | 4 | -0.046681 | 12.612 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.063726 | 17.979 |
| w22 | 2 | -0.087898 | 2.905 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.124171 | -1.113 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.0018 | 1.202 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.028281 | 1.048 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.070633 | -0.569 |
| w9 | 0 | None | 0.0 |
| w10 | 1 | 0.22848 | 6.565 |
| w11 | 3 | -0.010922 | 3.389 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.002312 | -6.744 |
| w14 | 3 | 0.069303 | -1.064 |
| w15 | 1 | -0.24341 | -1.531 |
| w16 | 2 | -0.034831 | 3.763 |
| w17 | 2 | 0.010323 | -0.864 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | -0.058951 | 0.0 |
| w20 | 2 | 0.032395 | 3.224 |
| w21 | 1 | -0.059822 | -3.425 |
| w22 | 2 | 0.088792 | -1.162 |
| w23 | 1 | 0.08488 | 9.288 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | 0.059444 | 1.048 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.052003 | -6.482 |
| w8 | 2 | -0.088587 | 1.952 |
| w9 | 2 | 0.095295 | -1.055 |
| w10 | 1 | -0.059054 | -2.499 |
| w11 | 6 | 0.136505 | 18.291 |
| w12 | 1 | -0.0295 | -11.102 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.074987 | -2.682 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.070153 | -1.228 |
| w18 | 1 | -0.036466 | -2.608 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | -0.047399 | 0.0 |
| w21 | 2 | -0.010567 | -0.463 |
| w22 | 2 | 0.051494 | -2.165 |
| w23 | 2 | -0.125321 | -3.14 |
| w24 | 4 | 0.224116 | 11.569 |

