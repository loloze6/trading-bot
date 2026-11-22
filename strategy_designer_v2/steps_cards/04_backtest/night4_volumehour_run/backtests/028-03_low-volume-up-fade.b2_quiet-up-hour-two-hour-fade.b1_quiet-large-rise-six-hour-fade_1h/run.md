# Backtest of 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h

- Plan: `../../../../03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH as BTCUSD, ETHUSD; 1h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 316 | 0.000659 | 15.231 |
| w2 | 288 | -0.013879 | -18.744 |
| w3 | 288 | 0.001184 | 34.512 |
| w4 | 337 | 0.001125 | -52.854 |
| w5 | 333 | 0.024169 | -1.142 |
| w6 | 340 | 0.021584 | -40.605 |
| w7 | 331 | 0.033938 | -4.612 |
| w8 | 327 | -0.004318 | -32.613 |
| w9 | 314 | 0.022057 | -22.164 |
| w10 | 383 | -0.009934 | -35.672 |
| w11 | 456 | -0.019015 | -20.237 |
| w12 | 367 | -0.004077 | -7.151 |
| w13 | 377 | 0.015599 | 1.158 |
| w14 | 267 | 0.027116 | 29.397 |
| w15 | 386 | -0.01109 | -22.238 |
| w16 | 331 | -0.002187 | -8.211 |
| w17 | 425 | 0.026128 | -24.817 |
| w18 | 413 | -0.015256 | -0.512 |
| w19 | 338 | 0.011118 | -22.422 |
| w20 | 300 | 0.012357 | -5.022 |
| w21 | 369 | -0.01387 | -34.891 |
| w22 | 307 | -0.007968 | 3.769 |
| w23 | 393 | -0.026692 | -35.004 |
| w24 | 324 | -0.013417 | -18.994 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 350 | 0.018673 | -3.588 |
| w2 | 334 | -0.047617 | -19.294 |
| w3 | 313 | -0.014497 | -17.878 |
| w4 | 295 | -0.01528 | -44.633 |
| w5 | 276 | 0.00439 | -0.245 |
| w6 | 325 | 0.02811 | 11.035 |
| w7 | 346 | 0.011134 | -13.279 |
| w8 | 283 | 0.018695 | -26.885 |
| w9 | 292 | 0.011756 | -11.311 |
| w10 | 355 | 0.006419 | -44.784 |
| w11 | 413 | -0.005206 | -26.421 |
| w12 | 374 | -0.000522 | -22.301 |
| w13 | 179 | 0.007024 | -21.577 |
| w14 | 265 | -0.011444 | -4.473 |
| w15 | 296 | 0.021003 | -8.312 |
| w16 | 348 | -0.002612 | -41.113 |
| w17 | 387 | 0.00101 | -16.632 |
| w18 | 392 | -0.011998 | -13.45 |
| w19 | 356 | -0.010251 | -31.881 |
| w20 | 272 | 0.010177 | -7.868 |
| w21 | 299 | 0.044495 | 0.004 |
| w22 | 296 | 0.019486 | 27.736 |
| w23 | 415 | -0.022833 | -44.495 |
| w24 | 278 | 0.011642 | 38.867 |

