# Backtest of 031-02.b1_wide-flat-day-continues-uprun_1d

- Plan: `../../../../03_test_plan/night6_indecision_run/plans/031-02.b1_wide-flat-day-continues-uprun_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.026455 | -1.904 |
| w4 | 2 | -0.085755 | 17.601 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.086126 | 3.883 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.008273 | 1.906 |
| w17 | 3 | 0.036716 | 10.487 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.023195 | -6.718 |
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
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | 0.060934 | 0.204 |
| w8 | 2 | 0.115786 | 0.596 |
| w9 | 2 | 0.056854 | -4.768 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.047288 | 3.993 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 6 | 0.038207 | 26.844 |
| w17 | 2 | -0.041214 | 4.178 |
| w18 | 2 | 0.074844 | -24.279 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.146703 | 5.413 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.118538 | -3.087 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 3 | -0.096454 | 6.014 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.062461 | -0.803 |
| w9 | 2 | 0.135319 | 2.656 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | 0.026641 | 6.181 |
| w12 | 2 | 0.016996 | -11.113 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.050407 | 8.864 |
| w16 | 4 | -0.014878 | -7.173 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.150209 | 34.634 |
| w20 | 1 | -0.012447 | -0.302 |
| w21 | 2 | -0.006307 | -9.331 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.183507 | 21.955 |
| w24 | 2 | 0.005353 | -22.099 |

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
| w9 | 1 | -0.076137 | -3.109 |
| w10 | 1 | 0.090713 | 35.033 |
| w11 | 4 | -0.003676 | 2.94 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.016794 | 7.463 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.063726 | 16.818 |
| w22 | 2 | -0.086236 | -0.116 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.165947 | 7.055 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.0018 | 9.261 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.028281 | 0.315 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.070633 | -1.246 |
| w9 | 2 | -0.150661 | 0.106 |
| w10 | 2 | 0.22848 | -2.652 |
| w11 | 2 | 0.000167 | -8.487 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | 0.002289 | 11.695 |
| w14 | 4 | 0.069303 | -2.256 |
| w15 | 1 | -0.24341 | -4.894 |
| w16 | 2 | -0.034831 | -6.073 |
| w17 | 2 | 0.010323 | -4.221 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.058951 | 6.689 |
| w20 | 0 | 0.032395 | 0.0 |
| w21 | 2 | -0.059822 | 48.899 |
| w22 | 2 | 0.088792 | -1.715 |
| w23 | 1 | 0.08488 | 42.099 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.052003 | 4.769 |
| w8 | 2 | -0.088587 | 0.085 |
| w9 | 2 | 0.095295 | 0.483 |
| w10 | 1 | -0.059054 | -10.182 |
| w11 | 4 | 0.153755 | -6.105 |
| w12 | 1 | -0.0295 | -2.317 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.061228 | 6.716 |
| w18 | 1 | -0.036466 | -12.228 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.047399 | -0.061 |
| w21 | 2 | -0.010567 | 4.648 |
| w22 | 2 | 0.051494 | -1.674 |
| w23 | 4 | -0.138571 | -8.448 |
| w24 | 4 | 0.228472 | 8.742 |

