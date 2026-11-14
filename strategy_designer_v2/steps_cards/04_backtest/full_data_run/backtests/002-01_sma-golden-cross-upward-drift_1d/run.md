# Backtest of 002-01_sma-golden-cross-upward-drift_1d

- Plan: `../../../../03_test_plan/full_data_run/plans/002-01_sma-golden-cross-upward-drift_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.108713 | -8.145 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 8 | -0.080007 | 25.073 |
| w5 | 9 | -0.008243 | -9.038 |
| w6 | 10 | -0.044291 | 26.16 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.002073 | 0.54 |
| w9 | 5 | -0.027301 | -13.928 |
| w10 | 12 | -0.055668 | 22.215 |
| w11 | 14 | 0.072998 | 198.708 |
| w12 | 14 | -0.139142 | -40.283 |
| w13 | 11 | -0.067947 | -48.781 |
| w14 | 0 | None | 0.0 |
| w15 | 21 | -0.10404 | 54.721 |
| w16 | 3 | -0.190551 | -11.831 |
| w17 | 17 | -0.078645 | 216.934 |
| w18 | 5 | -0.160788 | -26.3 |
| w19 | 9 | -0.063584 | 61.663 |
| w20 | 7 | 0.086395 | 9.893 |
| w21 | 8 | -0.097559 | 6.65 |
| w22 | 10 | -0.055276 | -13.488 |
| w23 | 7 | -0.129578 | -6.336 |
| w24 | 7 | 0.091348 | -2.742 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.156826 | -26.106 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 7 | -0.084276 | 10.002 |
| w5 | 9 | 0.043876 | -5.791 |
| w6 | 8 | -0.032823 | 5.67 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | -0.029584 | 0.0 |
| w9 | 0 | 0.079315 | 0.0 |
| w10 | 10 | 0.039465 | 149.245 |
| w11 | 16 | -0.101054 | 470.054 |
| w12 | 5 | -0.06319 | -9.538 |
| w13 | 13 | -0.148232 | -59.23 |
| w14 | 0 | None | 0.0 |
| w15 | 16 | -0.12512 | -35.955 |
| w16 | 13 | -0.181128 | -73.198 |
| w17 | 11 | -0.175529 | 7.905 |
| w18 | 6 | -0.098945 | -25.618 |
| w19 | 13 | 0.10198 | 46.182 |
| w20 | 6 | 0.084848 | 7.297 |
| w21 | 6 | -0.130452 | -14.16 |
| w22 | 7 | 0.005007 | -24.603 |
| w23 | 10 | -0.034601 | 29.125 |
| w24 | 10 | 0.007108 | -32.478 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.062519 | -6.785 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.063646 | -3.054 |
| w4 | 10 | -0.104492 | 0.55 |
| w5 | 4 | -0.035361 | -1.113 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 6 | -0.07699 | -2.592 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.005181 | 1.781 |
| w11 | 13 | -0.031637 | 180.701 |
| w12 | 7 | -0.138284 | -32.4 |
| w13 | 11 | -0.065558 | -55.738 |
| w14 | 0 | None | 0.0 |
| w15 | 13 | 0.126813 | 2.584 |
| w16 | 7 | -0.180565 | -21.558 |
| w17 | 25 | -0.01804 | 67.355 |
| w18 | 6 | -0.076772 | -48.599 |
| w19 | 12 | -0.07376 | -30.662 |
| w20 | 8 | 0.039351 | -2.539 |
| w21 | 11 | -0.08959 | -26.962 |
| w22 | 14 | 0.014132 | -29.083 |
| w23 | 5 | -0.104101 | -10.083 |
| w24 | 10 | 0.012278 | -22.948 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.106925 | -1.474 |
| w2 | 4 | -0.025423 | -10.175 |
| w3 | 0 | None | 0.0 |
| w4 | 10 | -0.126729 | -5.626 |
| w5 | 9 | -0.140699 | -10.895 |
| w6 | 10 | -0.080497 | -2.611 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.04077 | -3.16 |
| w10 | 8 | -0.009748 | 20.729 |
| w11 | 6 | -0.081448 | 272.203 |
| w12 | 0 | -0.1062 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.071746 | -24.645 |
| w16 | 10 | -0.205681 | -43.082 |
| w17 | 8 | -0.027036 | 103.788 |
| w18 | 13 | -0.075274 | -76.127 |
| w19 | 9 | -0.049882 | -26.0 |
| w20 | 10 | -0.11301 | -1.126 |
| w21 | 11 | -0.124754 | -11.344 |
| w22 | 10 | -0.15957 | 39.776 |
| w23 | 15 | -0.018572 | -15.358 |
| w24 | 10 | -0.038595 | 6.453 |

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 364 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XRPUSD: 22 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.089675 | -11.383 |
| w4 | 8 | -0.080511 | -10.863 |
| w5 | 10 | -0.229408 | -21.424 |
| w6 | 13 | -0.082067 | -1.427 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | -0.066563 | -7.112 |
| w11 | 26 | -0.029302 | 491.575 |
| w12 | 7 | -0.060063 | -5.94 |
| w14 | 0 | None | 0.0 |
| w15 | 15 | -0.122067 | -43.505 |
| w16 | 0 | -0.20523 | 0.0 |
| w17 | 22 | -0.190029 | -93.442 |
| w18 | 21 | -0.143084 | -87.791 |
| w19 | 13 | -0.132533 | -28.984 |
| w20 | 4 | -0.06175 | -3.589 |
| w21 | 16 | -0.009212 | 280.492 |
| w22 | 16 | 0.011399 | -19.994 |
| w23 | 5 | -0.107489 | -8.169 |
| w24 | 6 | 0.028116 | -17.765 |

- w7 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 347 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w13 not run: the engine stopped.

```
  File "/home/user/trading-bot/trading-bot/core/launcher.py", line 1037, in run_backtest
    assert probe.is_ready(), (
           ~~~~~~~~~~~~~~^^
AssertionError: warmup_prefetch: strategy not ready after 228 prefetch bars (<date> to <date>) -- required_bars=250. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.122744 | -23.13 |
| w2 | 2 | -0.105727 | -15.912 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.15364 | -5.956 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | -0.045065 | 12.006 |
| w11 | 28 | -0.122503 | 224.391 |
| w12 | 6 | -0.113841 | -46.094 |
| w13 | 11 | -0.060858 | -64.239 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | -0.15444 | -50.373 |
| w16 | 12 | -0.247004 | -64.13 |
| w17 | 14 | -0.086936 | -55.943 |
| w18 | 19 | -0.068301 | -88.292 |
| w19 | 11 | -0.151941 | -30.55 |
| w20 | 8 | -0.166778 | -41.081 |
| w21 | 22 | -0.071163 | 79.101 |
| w22 | 13 | -0.117074 | -59.883 |
| w23 | 3 | -0.044575 | 1.19 |
| w24 | 39 | -0.020875 | 1401.122 |

