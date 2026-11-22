# Backtest of 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h

- Plan: `../../../../03_test_plan/night4_panic_run/plans/027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | -0.007934 | 18.278 |
| w9 | 0 | 0.001441 | 0.0 |
| w10 | 3 | -0.013419 | 16.682 |
| w11 | 2 | 0.008295 | 10.57 |
| w12 | 4 | 0.036185 | -8.9 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.032571 | 19.617 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.153311 | 6.782 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.036917 | 7.816 |
| w22 | 2 | -0.044797 | -2.317 |
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
| w7 | 0 | None | 0.0 |
| w8 | 3 | -0.031831 | -0.041 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.01887 | 45.762 |
| w11 | 5 | -0.01084 | 65.304 |
| w12 | 2 | 0.003279 | -14.011 |
| w13 | 0 | 0.069883 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.014078 | 25.869 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.082867 | 14.629 |
| w18 | 2 | 0.101435 | 6.886 |
| w19 | 2 | 0.192206 | -1.324 |
| w20 | 1 | 0.024526 | 4.039 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.103829 | 2.117 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.000134 | 3.201 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.024121 | -5.269 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.020771 | 5.709 |
| w11 | 2 | 0.020999 | 0.609 |
| w12 | 1 | -0.014419 | -13.903 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.02507 | 21.048 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.090222 | -9.734 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.011465 | 19.21 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.017487 | -1.605 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.036228 | 2.363 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.045731 | 12.851 |
| w11 | 5 | 0.132734 | 17.369 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.131382 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.030878 | 24.748 |
| w16 | 4 | 0.035177 | -9.411 |
| w17 | 2 | 0.01754 | 13.742 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.029955 | 1.323 |
| w21 | 2 | -0.01627 | -3.073 |
| w22 | 2 | -0.068256 | 0.126 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | -0.007325 | 44.787 |
| w4 | 1 | 0.055307 | 26.712 |
| w5 | 4 | 0.016881 | 1.524 |
| w6 | 2 | 0.038811 | -2.66 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.072022 | 3.918 |
| w11 | 4 | -0.007654 | 41.845 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.014221 | -13.483 |
| w14 | 5 | 0.012402 | -21.715 |
| w15 | 4 | 0.002808 | 32.611 |
| w16 | 2 | 0.043546 | -30.442 |
| w17 | 3 | -0.044343 | 21.7 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.016856 | -2.12 |
| w20 | 2 | -0.053197 | 5.77 |
| w21 | 6 | 0.060329 | 239.99 |
| w22 | 4 | 0.142707 | -3.69 |
| w23 | 1 | 0.05196 | 24.062 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.011812 | -4.702 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.031199 | 2.438 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | 0.037082 | 3.7 |
| w11 | 8 | 0.152222 | 4.081 |
| w12 | 2 | 0.049237 | 16.347 |
| w13 | 0 | 0.093077 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.010251 | 8.884 |
| w16 | 3 | -0.020694 | 13.752 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.059477 | -24.569 |
| w19 | 2 | -0.016054 | -13.48 |
| w20 | 2 | -0.031819 | 28.028 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | 0.146686 | 278.257 |

