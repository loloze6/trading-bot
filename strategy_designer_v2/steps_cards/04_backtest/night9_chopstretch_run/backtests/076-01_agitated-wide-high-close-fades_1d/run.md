# Backtest of 076-01_agitated-wide-high-close-fades_1d

- Plan: `../../../../03_test_plan/night9_chopstretch_run/plans/076-01_agitated-wide-high-close-fades_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.019436 | 1.274 |
| w2 | 10 | 0.023389 | 7.751 |
| w3 | 11 | 0.163968 | 20.586 |
| w4 | 6 | -0.090353 | -12.853 |
| w5 | 0 | None | 0.0 |
| w6 | 14 | 0.096192 | 0.632 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | -0.002887 | -0.973 |
| w9 | 5 | -0.075836 | -5.599 |
| w10 | 4 | 0.137649 | 7.127 |
| w11 | 26 | 0.029881 | -17.24 |
| w12 | 12 | -0.141617 | -18.296 |
| w13 | 13 | 0.011867 | 2.488 |
| w14 | 6 | 0.134858 | 18.622 |
| w15 | 25 | 0.084882 | -1.189 |
| w16 | 11 | 0.047748 | 2.976 |
| w17 | 15 | 0.013272 | -10.002 |
| w18 | 13 | 0.000855 | -3.272 |
| w19 | 25 | 0.128211 | 7.406 |
| w20 | 17 | 0.078331 | 7.437 |
| w21 | 14 | 0.082535 | 0.967 |
| w22 | 10 | 0.149655 | 17.805 |
| w23 | 1 | -0.019229 | -0.635 |
| w24 | 15 | 0.128107 | 20.407 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.032396 | -1.912 |
| w2 | 15 | -0.031279 | -3.281 |
| w3 | 7 | 0.051026 | 4.919 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 12 | 0.173792 | 15.883 |
| w7 | 0 | None | 0.0 |
| w8 | 5 | 0.126088 | 5.736 |
| w9 | 4 | -0.015193 | -1.273 |
| w10 | 6 | 0.009846 | -4.441 |
| w11 | 22 | -0.028066 | -29.854 |
| w12 | 6 | 0.011344 | 0.356 |
| w13 | 9 | -0.12212 | -12.463 |
| w14 | 15 | 0.078156 | 20.228 |
| w15 | 9 | 0.02682 | 1.256 |
| w16 | 15 | 0.204059 | 26.289 |
| w17 | 12 | 0.048616 | -0.674 |
| w18 | 12 | 0.178083 | 22.92 |
| w19 | 14 | 0.021613 | -4.738 |
| w20 | 16 | 0.025272 | 5.432 |
| w21 | 20 | 0.036315 | -6.419 |
| w22 | 17 | 0.29736 | 68.326 |
| w23 | 10 | -0.02236 | -9.787 |
| w24 | 8 | -0.002422 | 1.337 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 7 | 0.010409 | 4.885 |
| w3 | 6 | -0.127074 | -11.429 |
| w4 | 6 | -0.038779 | -5.789 |
| w5 | 10 | 0.087536 | 7.762 |
| w6 | 2 | -0.009235 | -1.395 |
| w7 | 0 | None | 0.0 |
| w8 | 17 | 0.058361 | -2.192 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.029807 | 0.413 |
| w11 | 21 | 0.081565 | 0.436 |
| w12 | 4 | 0.021664 | 1.097 |
| w13 | 7 | 0.047179 | 2.396 |
| w14 | 12 | 0.018921 | 2.93 |
| w15 | 13 | -0.063371 | -9.683 |
| w16 | 8 | 0.088036 | 6.314 |
| w17 | 18 | -0.05536 | -16.006 |
| w18 | 8 | -0.036679 | -6.21 |
| w19 | 11 | 0.165593 | 14.454 |
| w20 | 11 | 0.085319 | 9.291 |
| w21 | 24 | -0.031387 | -24.882 |
| w22 | 18 | 0.040408 | 2.768 |
| w23 | 1 | 0.031273 | 0.825 |
| w24 | 6 | 0.01192 | 2.643 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.147808 | 15.122 |
| w2 | 7 | 0.068067 | 8.146 |
| w3 | 2 | 0.005516 | -0.199 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 5 | -0.066906 | -7.524 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.154776 | 4.718 |
| w9 | 1 | -0.011145 | -0.138 |
| w10 | 3 | 0.128767 | 5.838 |
| w11 | 19 | 0.16995 | 3.379 |
| w12 | 5 | -0.022082 | -2.386 |
| w14 | 6 | 0.114599 | 12.946 |
| w15 | 11 | 0.351311 | 51.927 |
| w16 | 11 | 0.019667 | -2.935 |
| w17 | 19 | 0.128649 | 8.277 |
| w18 | 3 | 0.022818 | 0.14 |
| w19 | 22 | 0.039264 | 8.941 |
| w20 | 13 | -0.071079 | -18.559 |
| w21 | 7 | 0.35098 | 39.685 |
| w22 | 13 | -0.022792 | -11.725 |
| w23 | 15 | 0.034572 | -4.16 |
| w24 | 15 | -0.050937 | -15.857 |

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.076426 | 4.822 |
| w2 | 1 | 0.016829 | 15.914 |
| w3 | 0 | 0.088372 | 0.0 |
| w4 | 0 | 0.123001 | 0.0 |
| w5 | 5 | 0.129499 | 6.729 |
| w6 | 5 | 0.029875 | 0.13 |
| w8 | 0 | None | 0.0 |
| w9 | 8 | 0.133937 | 17.091 |
| w10 | 2 | -0.095888 | -7.054 |
| w11 | 19 | 0.04724 | -24.496 |
| w12 | 1 | 0.017503 | 0.361 |
| w14 | 9 | -0.169307 | -16.768 |
| w15 | 8 | -0.049694 | -6.332 |
| w16 | 15 | 0.101242 | 9.415 |
| w17 | 13 | 0.011555 | -0.576 |
| w18 | 8 | 0.208694 | 13.959 |
| w19 | 9 | 0.148817 | 14.645 |
| w20 | 12 | -0.097286 | -21.979 |
| w21 | 17 | -0.253303 | -48.304 |
| w22 | 22 | 0.134687 | 19.441 |
| w23 | 3 | -0.03379 | -3.237 |
| w24 | 5 | -0.001465 | 0.522 |

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 347 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | 0.05599 | 4.859 |
| w2 | 9 | 0.092043 | 10.549 |
| w3 | 3 | -0.103551 | -7.45 |
| w4 | 1 | 0.139423 | 4.984 |
| w5 | 7 | -0.006259 | -2.144 |
| w6 | 6 | 0.034877 | 0.845 |
| w7 | 1 | 0.023065 | 0.618 |
| w8 | 1 | 0.046663 | 0.801 |
| w9 | 7 | 0.210245 | 28.156 |
| w10 | 8 | 0.103056 | 6.197 |
| w11 | 22 | -0.034364 | -27.222 |
| w12 | 7 | -0.132742 | -19.6 |
| w13 | 10 | -0.012779 | -0.557 |
| w14 | 6 | 0.235873 | 27.054 |
| w15 | 10 | -0.12425 | -13.137 |
| w16 | 26 | 0.075393 | -17.335 |
| w17 | 9 | 0.102363 | 15.222 |
| w18 | 8 | -0.024011 | -3.23 |
| w19 | 22 | -0.055428 | -11.977 |
| w20 | 26 | -0.143951 | -33.674 |
| w21 | 18 | -0.056948 | -19.87 |
| w22 | 15 | -0.084123 | -11.639 |
| w23 | 6 | -0.087055 | -10.264 |
| w24 | 29 | -0.223966 | -71.136 |

