# Backtest of 032-02_flat-range-downside-break-recovers_1d

- Plan: `../../../../03_test_plan/night7c_rangefail_run/plans/032-02_flat-range-downside-break-recovers_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.089984 | 1.444 |
| w2 | 4 | -0.004807 | -2.333 |
| w3 | 2 | 0.342138 | 3.14 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | 0.169243 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | 0.116075 | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | -0.010152 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.184739 | 0.0 |
| w14 | 2 | -0.138266 | -25.649 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | 0.264057 | 6.505 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.211695 | 3.738 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | -0.006614 | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | -0.00852 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.01316 | -1.666 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.125614 | 1.201 |
| w2 | 3 | -0.07418 | -11.059 |
| w3 | 2 | 0.417655 | 1.813 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | 0.023006 | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.07108 | -5.312 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.237367 | 1.001 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.034498 | 0.0 |
| w14 | 3 | -0.055092 | -9.049 |
| w15 | 0 | 0.101688 | 0.0 |
| w16 | 2 | 0.310162 | 6.198 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.07746 | -0.968 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | 0.018451 | -2.722 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.07257 | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.087642 | -0.472 |
| w2 | 4 | 0.044696 | -1.505 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | -0.075926 | 0.0 |
| w5 | 2 | -0.056207 | -0.252 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.051689 | -2.422 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.138541 | 1.611 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.067811 | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | -0.020332 | -7.172 |
| w15 | 0 | -0.07546 | 0.0 |
| w16 | 2 | 0.355445 | 6.166 |
| w17 | 0 | 0.039301 | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.112534 | 1.439 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.013329 | 3.078 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | -0.070735 | 0.0 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.006029 | -0.977 |
| w2 | 0 | -0.100718 | 0.0 |
| w3 | 2 | 0.328904 | 5.799 |
| w4 | 0 | 0.142716 | 0.0 |
| w5 | 2 | 0.206207 | -1.185 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | 0.162825 | -1.583 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.089465 | -0.985 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | -0.093344 | -5.355 |
| w15 | 2 | 0.033787 | 0.094 |
| w16 | 2 | 0.216413 | 7.358 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.458959 | 12.635 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | 0.133737 | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.036537 | 0.0 |
| w2 | 2 | 0.099383 | -3.932 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | -0.209731 | -0.932 |
| w8 | 0 | 0.072038 | 0.0 |
| w9 | 2 | 0.199022 | 0.923 |
| w10 | 0 | 0.021334 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | -0.097405 | 0.0 |
| w13 | 0 | -0.000366 | 0.0 |
| w14 | 0 | -0.018224 | 0.0 |
| w15 | 2 | 0.021227 | -0.223 |
| w16 | 2 | 0.274054 | 2.263 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | 0.09669 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | 0.000167 | 0.0 |
| w21 | 0 | 0.016047 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.024741 | 1.259 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.154711 | -0.76 |
| w2 | 0 | 0.030156 | 0.0 |
| w3 | 1 | -0.212529 | -4.559 |
| w4 | 0 | -0.17339 | 0.0 |
| w5 | 2 | 0.080231 | 4.625 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.015529 | 0.471 |
| w8 | 0 | 0.015995 | 0.0 |
| w9 | 2 | 0.065611 | -0.618 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | 0.032118 | 0.0 |
| w13 | 0 | 0.100466 | 0.0 |
| w14 | 4 | 0.073804 | -7.194 |
| w15 | 0 | 0.019391 | 0.0 |
| w16 | 2 | 0.087169 | 3.771 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.018822 | -0.998 |
| w20 | 2 | -0.003129 | 13.417 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.083123 | 0.664 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

