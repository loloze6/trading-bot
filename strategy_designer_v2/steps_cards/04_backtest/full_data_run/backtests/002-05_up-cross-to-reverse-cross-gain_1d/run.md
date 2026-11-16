# Backtest of 002-05_up-cross-to-reverse-cross-gain_1d

- Plan: `../../../../03_test_plan/full_data_run/plans/002-05_up-cross-to-reverse-cross-gain_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | -0.108713 | -4.146 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 8 | -0.080007 | 17.961 |
| w5 | 9 | -0.008243 | -6.021 |
| w6 | 11 | -0.044291 | 23.224 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.002073 | 0.369 |
| w9 | 5 | -0.027301 | -10.638 |
| w10 | 12 | -0.055668 | 18.233 |
| w11 | 6 | 0.072998 | 83.814 |
| w12 | 14 | -0.139142 | -24.925 |
| w13 | 8 | -0.067947 | -13.719 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.10404 | 43.894 |
| w16 | 4 | -0.190551 | -9.69 |
| w17 | 13 | -0.078645 | 138.005 |
| w18 | 5 | -0.160788 | -16.024 |
| w19 | 7 | -0.063584 | 58.883 |
| w20 | 7 | 0.086395 | 7.55 |
| w21 | 8 | -0.097559 | 9.136 |
| w22 | 12 | -0.055276 | -14.183 |
| w23 | 10 | -0.129578 | -7.842 |
| w24 | 10 | 0.091348 | -1.164 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.156826 | -12.586 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 8 | -0.084276 | 7.182 |
| w5 | 10 | 0.043876 | -4.111 |
| w6 | 8 | -0.032823 | 3.487 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | -0.029584 | 0.0 |
| w9 | 0 | 0.079315 | 0.0 |
| w10 | 9 | 0.039465 | 73.48 |
| w11 | 6 | -0.101054 | 135.911 |
| w12 | 7 | -0.06319 | -7.13 |
| w13 | 12 | -0.148232 | -13.912 |
| w14 | 0 | None | 0.0 |
| w15 | 15 | -0.12512 | -9.424 |
| w16 | 12 | -0.181128 | -28.567 |
| w17 | 9 | -0.175529 | 12.924 |
| w18 | 7 | -0.098945 | -8.166 |
| w19 | 8 | 0.10198 | 35.656 |
| w20 | 7 | 0.084848 | 1.183 |
| w21 | 6 | -0.130452 | -7.13 |
| w22 | 8 | 0.005007 | -16.117 |
| w23 | 8 | -0.034601 | 20.335 |
| w24 | 10 | 0.007108 | -19.096 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.062519 | -2.528 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.063646 | -0.807 |
| w4 | 10 | -0.104492 | 2.904 |
| w5 | 4 | -0.035361 | -1.378 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | -0.07699 | 1.099 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.005181 | 0.951 |
| w11 | 4 | -0.031637 | 60.184 |
| w12 | 5 | -0.138284 | -13.155 |
| w13 | 9 | -0.065558 | -5.691 |
| w14 | 0 | None | 0.0 |
| w15 | 10 | 0.126813 | 8.073 |
| w16 | 5 | -0.180565 | -10.386 |
| w17 | 19 | -0.01804 | 29.365 |
| w18 | 6 | -0.076772 | -18.359 |
| w19 | 8 | -0.07376 | -7.143 |
| w20 | 9 | 0.039351 | -2.927 |
| w21 | 7 | -0.08959 | -3.832 |
| w22 | 10 | 0.014132 | -10.062 |
| w23 | 5 | -0.104101 | -5.752 |
| w24 | 10 | 0.012278 | -13.807 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.106925 | -0.506 |
| w2 | 4 | -0.025423 | -4.224 |
| w3 | 0 | None | 0.0 |
| w4 | 10 | -0.126729 | -10.842 |
| w5 | 14 | -0.140699 | -16.602 |
| w6 | 11 | -0.080497 | -1.96 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.04077 | -2.528 |
| w10 | 10 | -0.009748 | 13.287 |
| w11 | 6 | -0.081448 | 82.452 |
| w12 | 0 | -0.1062 | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 12 | -0.071746 | -5.941 |
| w16 | 8 | -0.205681 | -17.351 |
| w17 | 4 | -0.027036 | 50.503 |
| w18 | 11 | -0.075274 | -26.438 |
| w19 | 10 | -0.049882 | -28.048 |
| w20 | 10 | -0.11301 | 0.678 |
| w21 | 10 | -0.124754 | -4.415 |
| w22 | 11 | -0.15957 | 22.507 |
| w23 | 15 | -0.018572 | -4.855 |
| w24 | 10 | -0.038595 | 5.39 |

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
| w3 | 4 | -0.089675 | -3.923 |
| w4 | 8 | -0.080511 | -4.788 |
| w5 | 6 | -0.229408 | 76.168 |
| w6 | 14 | -0.082067 | 2.851 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 8 | -0.066563 | -4.339 |
| w11 | 17 | -0.029302 | 73.672 |
| w12 | 3 | -0.060063 | -4.175 |
| w14 | 0 | None | 0.0 |
| w15 | 13 | -0.122067 | -15.722 |
| w16 | 0 | -0.20523 | 0.0 |
| w17 | 12 | -0.190029 | -12.134 |
| w18 | 10 | -0.143084 | -22.745 |
| w19 | 13 | -0.132533 | -15.595 |
| w20 | 4 | -0.06175 | -1.635 |
| w21 | 13 | -0.009212 | 108.406 |
| w22 | 10 | 0.011399 | 1.758 |
| w23 | 5 | -0.107489 | -4.208 |
| w24 | 7 | 0.028116 | -13.1 |

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
| w1 | 7 | -0.122744 | -6.235 |
| w2 | 2 | -0.105727 | -3.243 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.15364 | -4.566 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 9 | -0.045065 | 9.427 |
| w11 | 9 | -0.122503 | 62.038 |
| w12 | 6 | -0.113841 | -13.26 |
| w13 | 12 | -0.060858 | -15.706 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.15444 | -19.653 |
| w16 | 11 | -0.247004 | -18.434 |
| w17 | 10 | -0.086936 | -20.449 |
| w18 | 10 | -0.068301 | -31.753 |
| w19 | 12 | -0.151941 | -16.486 |
| w20 | 6 | -0.166778 | -17.334 |
| w21 | 13 | -0.071163 | 48.857 |
| w22 | 9 | -0.117074 | -20.848 |
| w23 | 3 | -0.044575 | 0.526 |
| w24 | 10 | -0.020875 | 196.611 |

