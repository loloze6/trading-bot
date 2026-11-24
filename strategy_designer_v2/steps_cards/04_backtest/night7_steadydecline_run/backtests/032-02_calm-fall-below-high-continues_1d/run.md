# Backtest of 032-02_calm-fall-below-high-continues_1d

- Plan: `../../../../03_test_plan/night7_steadydecline_run/plans/032-02_calm-fall-below-high-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.060985 | -5.653 |
| w2 | 8 | 0.158863 | 18.593 |
| w3 | 11 | 0.109187 | -8.415 |
| w4 | 1 | 0.013613 | -0.692 |
| w5 | 8 | -0.055791 | -6.044 |
| w6 | 10 | 0.074221 | 0.218 |
| w7 | 24 | -0.029526 | 9.463 |
| w8 | 4 | 0.055937 | 0.711 |
| w9 | 26 | -0.138703 | -20.45 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.034784 | 5.477 |
| w12 | 8 | -0.00478 | -0.504 |
| w13 | 11 | 0.000319 | -1.117 |
| w14 | 8 | 0.130452 | 38.534 |
| w15 | 0 | None | 0.0 |
| w16 | 4 | -0.089047 | -5.133 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.083692 | 0.748 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.022724 | -4.229 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.194144 | 13.709 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.020226 | 2.931 |
| w2 | 2 | -0.088467 | 12.316 |
| w3 | 11 | 0.069895 | 3.327 |
| w4 | 2 | -0.052566 | -1.309 |
| w5 | 7 | -0.039644 | -2.768 |
| w6 | 16 | 0.056353 | -7.003 |
| w7 | 20 | 0.000501 | 26.99 |
| w8 | 0 | None | 0.0 |
| w9 | 27 | -0.075794 | -2.342 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.0395 | 3.098 |
| w13 | 11 | 0.090596 | 8.516 |
| w14 | 7 | 0.22593 | 44.366 |
| w15 | 6 | 0.059984 | 4.683 |
| w16 | 3 | -0.057693 | -4.861 |
| w17 | 6 | -0.033721 | -4.157 |
| w18 | 4 | -0.028611 | -5.575 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 6 | 0.027218 | -3.337 |
| w22 | 5 | -0.019612 | 2.617 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | 0.047957 | 12.959 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | -0.123632 | 1.619 |
| w2 | 6 | 0.221747 | 20.537 |
| w3 | 11 | 0.010004 | -2.522 |
| w4 | 4 | -0.130335 | -18.449 |
| w5 | 4 | -0.083285 | 1.079 |
| w6 | 4 | 0.096616 | 4.881 |
| w7 | 31 | -0.04457 | 27.446 |
| w8 | 0 | None | 0.0 |
| w9 | 26 | -0.029187 | 14.662 |
| w10 | 7 | -0.02905 | -2.951 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | -0.010337 | -1.129 |
| w13 | 17 | -0.037913 | -6.753 |
| w14 | 19 | 0.075232 | 29.075 |
| w15 | 6 | 0.096025 | 10.612 |
| w16 | 8 | -0.115154 | -3.31 |
| w17 | 4 | -0.042344 | -4.031 |
| w18 | 3 | -0.023875 | -1.068 |
| w19 | 4 | -0.118965 | -14.455 |
| w20 | 13 | 0.031013 | 7.194 |
| w21 | 5 | -0.042549 | -4.873 |
| w22 | 1 | 0.121804 | 6.449 |
| w23 | 5 | -0.157278 | -7.299 |
| w24 | 6 | -0.044185 | -3.591 |

- XMRUSD: 23 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | -0.143942 | -11.086 |
| w2 | 3 | -0.121745 | -1.175 |
| w3 | 19 | -0.062831 | -9.002 |
| w4 | 11 | -0.304621 | -22.369 |
| w5 | 8 | -0.107587 | -7.761 |
| w6 | 9 | -0.033375 | -5.415 |
| w7 | 33 | -0.141421 | 2.618 |
| w8 | 2 | 0.065248 | 1.299 |
| w9 | 32 | -0.067474 | 4.572 |
| w10 | 3 | -0.14743 | -3.674 |
| w11 | 0 | None | 0.0 |
| w12 | 22 | -0.013364 | -1.938 |
| w14 | 11 | 0.146687 | 45.03 |
| w15 | 5 | 0.093639 | 6.088 |
| w16 | 4 | -0.139947 | -10.894 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.080965 | -2.879 |
| w19 | 0 | None | 0.0 |
| w20 | 7 | -0.100576 | -7.045 |
| w21 | 9 | -0.082168 | -10.728 |
| w22 | 6 | -0.147733 | -13.018 |
| w23 | 12 | 0.072322 | 12.239 |
| w24 | 3 | 0.011211 | -0.211 |

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
| w1 | 21 | 0.028815 | 3.183 |
| w2 | 4 | 0.000706 | 15.819 |
| w3 | 0 | 0.034896 | 0.0 |
| w4 | 0 | -0.003307 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.005076 | -0.465 |
| w8 | 19 | -0.051063 | 0.114 |
| w9 | 22 | 0.057308 | 15.98 |
| w10 | 6 | -0.10072 | -12.906 |
| w11 | 0 | None | 0.0 |
| w12 | 17 | -0.049197 | 0.797 |
| w14 | 20 | 0.005162 | -9.206 |
| w15 | 9 | 0.02898 | 4.491 |
| w16 | 2 | -0.109987 | -10.425 |
| w17 | 7 | -0.019016 | -1.928 |
| w18 | 3 | -0.000774 | -0.852 |
| w19 | 14 | -0.076041 | -11.907 |
| w20 | 11 | 0.087113 | 14.436 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.070931 | -1.485 |
| w23 | 2 | 0.027603 | 0.079 |
| w24 | 29 | -0.039929 | 8.345 |

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
| w1 | 23 | -0.086151 | -17.371 |
| w2 | 4 | -0.163387 | -3.273 |
| w3 | 24 | 0.099181 | 17.651 |
| w4 | 10 | -0.090514 | -13.719 |
| w5 | 22 | -0.036371 | 6.756 |
| w6 | 10 | -0.024305 | -5.243 |
| w7 | 24 | -0.076946 | 2.952 |
| w8 | 13 | 0.014392 | -0.937 |
| w9 | 19 | -0.076373 | -5.953 |
| w10 | 2 | -0.081071 | -10.542 |
| w11 | 0 | None | 0.0 |
| w12 | 3 | -0.052735 | -3.515 |
| w13 | 13 | 0.050194 | 7.243 |
| w14 | 20 | 0.064661 | 28.244 |
| w15 | 6 | 0.049794 | 10.01 |
| w16 | 0 | None | 0.0 |
| w17 | 12 | 0.018265 | -8.226 |
| w18 | 5 | -0.07667 | -5.06 |
| w19 | 0 | None | 0.0 |
| w20 | 8 | 0.061013 | -7.098 |
| w21 | 5 | -0.073541 | -9.011 |
| w22 | 2 | -0.180561 | -6.034 |
| w23 | 9 | -0.015375 | -3.708 |
| w24 | 0 | None | 0.0 |

