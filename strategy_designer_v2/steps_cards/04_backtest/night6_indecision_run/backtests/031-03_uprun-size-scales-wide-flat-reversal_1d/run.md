# Backtest of 031-03_uprun-size-scales-wide-flat-reversal_1d

- Plan: `../../../../03_test_plan/night6_indecision_run/plans/031-03_uprun-size-scales-wide-flat-reversal_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.07464 | 4.853 |
| w4 | 4 | 0.048417 | -16.254 |
| w5 | 0 | -0.019975 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.086126 | -0.248 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.008273 | -4.625 |
| w17 | 4 | -0.023737 | -12.601 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | 0.053342 | -0.557 |
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
| w4 | 0 | -0.060417 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | -0.060934 | 0.0 |
| w8 | 2 | -0.115786 | -0.414 |
| w9 | 2 | -0.056854 | -0.317 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.02178 | 0.056 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | 0.292994 | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 9 | -0.038103 | -27.73 |
| w17 | 0 | 0.041214 | 0.0 |
| w18 | 2 | -0.074844 | 3.306 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.14665 | -0.239 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.118538 | 1.732 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.093124 | 0.208 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.062461 | -1.667 |
| w9 | 2 | -0.135319 | -0.887 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.014017 | -6.044 |
| w12 | 2 | -0.016057 | -0.992 |
| w13 | 1 | 0.019202 | 0.274 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.050407 | 2.803 |
| w16 | 4 | 0.017091 | -1.527 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | -0.150209 | -28.754 |
| w20 | 1 | 0.012447 | 0.333 |
| w21 | 2 | 0.006307 | 16.095 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.16746 | -20.045 |
| w24 | 2 | -0.005353 | 1.841 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | -0.051566 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.076137 | 2.326 |
| w10 | 4 | -0.100222 | -23.893 |
| w11 | 4 | 0.046681 | -11.837 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.063726 | 1.742 |
| w22 | 2 | 0.087898 | -2.94 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.124171 | -1.973 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | 0.0018 | -3.136 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.028281 | -1.95 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.070633 | 5.769 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.22848 | -4.327 |
| w11 | 2 | 0.010922 | 0.556 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.002312 | 1.051 |
| w14 | 3 | -0.069303 | -10.758 |
| w15 | 1 | 0.24341 | 2.294 |
| w16 | 2 | 0.034831 | 0.257 |
| w17 | 2 | -0.010323 | 13.653 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | 0.058951 | 0.0 |
| w20 | 2 | -0.032395 | -3.238 |
| w21 | 2 | 0.059822 | -3.597 |
| w22 | 2 | -0.088792 | 1.128 |
| w23 | 3 | -0.08488 | -32.555 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 2 | -0.059444 | -1.528 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.052003 | 5.869 |
| w8 | 2 | 0.088587 | -5.885 |
| w9 | 2 | -0.095295 | 0.121 |
| w10 | 1 | 0.059054 | 7.944 |
| w11 | 7 | -0.136505 | -22.532 |
| w12 | 1 | 0.0295 | 4.629 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.074987 | 2.959 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.070153 | 2.464 |
| w18 | 1 | 0.036466 | 3.635 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.047399 | 0.0 |
| w21 | 2 | 0.010567 | 0.766 |
| w22 | 2 | -0.051494 | -0.253 |
| w23 | 2 | 0.125321 | 8.147 |
| w24 | 4 | -0.224116 | -9.16 |

