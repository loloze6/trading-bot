# Backtest of 012-04_flush-depth-retracement-size_1d

- Plan: `../../../../03_test_plan/night_012_run/plans/012-04_flush-depth-retracement-size_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.451455 | -22.327 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.10104 | -4.578 |
| w6 | 1 | 0.005941 | 0.774 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.005295 | 0.543 |
| w9 | 1 | -0.120483 | -3.799 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.031955 | -1.065 |
| w12 | 2 | -0.02533 | -1.806 |
| w13 | 1 | -0.045615 | -1.858 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.026621 | -0.28 |
| w18 | 1 | 0.213145 | 9.817 |
| w19 | 1 | 0.085598 | 5.099 |
| w20 | 2 | 0.147707 | 10.291 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.022724 | 1.169 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.022224 | 0.078 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.081763 | -2.382 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.390615 | -17.488 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | -0.053364 | -2.728 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.040754 | 1.331 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.025189 | 1.58 |
| w12 | 1 | 0.041546 | 1.702 |
| w13 | 1 | -0.058181 | -2.304 |
| w14 | 1 | 0.012122 | 0.222 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | 0.18178 | 8.13 |
| w19 | 1 | 0.065311 | 3.357 |
| w20 | 1 | 0.048607 | 2.308 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.026907 | 0.725 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 1 | -0.075926 | -3.377 |
| w5 | 2 | 0.037654 | 2.995 |
| w6 | 1 | -0.026028 | -1.031 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 1 | 0.022415 | 0.434 |
| w10 | 1 | -0.039698 | -0.663 |
| w11 | 1 | -0.077661 | -2.357 |
| w12 | 1 | -0.067811 | -2.987 |
| w13 | 1 | -0.018771 | -0.643 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.035415 | -0.917 |
| w18 | 1 | 0.169854 | 6.596 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.153079 | 10.364 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.099137 | -4.382 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.403392 | -18.172 |
| w4 | 1 | 0.140842 | 4.292 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.043929 | -1.532 |
| w7 | 2 | -0.039981 | -2.853 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.003125 | -0.226 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.138589 | 6.418 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.104871 | -7.095 |
| w20 | 1 | 0.01435 | 0.833 |
| w21 | 1 | -0.136982 | -8.901 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.070149 | 4.307 |
| w24 | 2 | -0.002323 | 0.328 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.343154 | -13.982 |
| w4 | 1 | -0.091102 | -3.051 |
| w5 | 1 | -0.005544 | -0.117 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.013989 | 0.273 |
| w10 | 1 | -0.072575 | -1.345 |
| w11 | 1 | -0.031237 | -0.601 |
| w12 | 2 | -0.096022 | -6.858 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.129789 | 4.457 |
| w15 | 1 | 0.019736 | 0.88 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.034317 | -2.752 |
| w20 | 1 | -0.036143 | -1.835 |
| w21 | 1 | 0.016047 | 3.227 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.020424 | 0.392 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.379077 | -18.203 |
| w4 | 0 | None | 0.0 |
| w5 | 5 | -0.080198 | -8.553 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.015995 | 0.191 |
| w9 | 2 | 0.09829 | 4.626 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | -0.004276 | -0.19 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | 0.183072 | 7.711 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.076315 | -4.75 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

